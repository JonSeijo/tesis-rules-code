# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import sys
import argparse
import re
import inspect
import ntpath
from pathlib import Path
from fastaread import Protein,FastaParser
from rulegroup import RuleGroupParser,Rule
from rulecoverage import RuleCoverage
from rule_stats_multithread import RuleStats
import sqlite3

from pathos.multiprocessing import ProcessingPool as Pool
# from multiprocessing import Pool


def insert_coverage_info_of_proteins(process_num, proteins, rules, dbfilename):
# def insert_coverage_info_of_proteins(parameters_list):
    # process_num, proteins, rules, dbfilename = parameters_list

    rs = RuleStats(dbfilename)
    cov = RuleCoverage("","","test.txt","vector")

    protein_amount = len(proteins)
    protein_count = 0

    toinsert_values = []

    for idProtein, protein in proteins:
        protein_count += 1
        if protein_count % 10 == 0:
            print(f"P{process_num} - {protein_count} / {protein_amount}")

        for idRule, rule in rules.items():
            coverageResult = cov.getCoverageOfRuleForProtein(protein, rule) #Single protein vs single rule
            fraction = coverageResult.getCoverageFraction()
            mode = coverageResult.getCoverageMode()

            if coverageResult.isProteinCovered(): #Stricter version!
                proteinStr = protein.getEncoding()
                ocurrenceType = rs.ocurrenceType(rule, proteinStr)
                antecedentRepeats = []
                antecedentRepeatsDistances = []
                antecedentAvgRepeatDistances = []
                consequentRepeats = rs.getOcurrencesIndexes(rule.consequent, proteinStr)
                consequentRepeatsDistances = rs.distanceBetweenConsecutiveRepeats(rule.consequent, proteinStr)
                
                consequentAvgRepeatDistance = rs.averageOcurrence(consequentRepeatsDistances)

                for ant in rule.antecedent:
                    antecedentRepeats.append(rs.getOcurrencesIndexes(ant, proteinStr))
                    ocurrs = rs.distanceBetweenConsecutiveRepeats(ant, proteinStr)
                    antecedentRepeatsDistances.append(ocurrs)
                    antecedentAvgRepeatDistances.append(rs.averageOcurrence(ocurrs))

                toInsert = (idRule, idProtein, fraction, mode, ocurrenceType, str(antecedentRepeats), str(consequentRepeats), str(consequentRepeatsDistances), consequentAvgRepeatDistance, str(antecedentRepeatsDistances), str(antecedentAvgRepeatDistances))
                toinsert_values.append(toInsert)
                # cursor.execute('''INSERT INTO rule_coverage(idRule, idProtein, fraction, coverageMode, consequentOcurrenceType, antecedentRepeats,
                #     consequentRepeats, consequentRepeatsDistances, consequentAvgRepeatDistance, antecedentRepeatsDistances, antecedentAvgRepeatDistances)
                #     VALUES (?,?,?,?,?,?,?,?,?,?,?)''', toInsert)

    return toinsert_values


class GenerateProteinRuleDb(object):
    """docstring for GenerateProteinRuleDb"""
    def __init__(self, filename="protein-rules.db"):
        super(GenerateProteinRuleDb, self).__init__()
        self.proteins = {}
        self.rules = {}
        self.filename = filename

    def createDB(self, proteinPath, ruleFile):
        """ Create a DB from scratch """
        # self.connection = self.createFile()
        self.insertProteins(proteinPath)
        self.insertRules(ruleFile)
        self.insertCoverageInfo(self.proteins, self.rules)
        self.insertItemInfo()
        # self.connection.close()

    def addProteins(self, proteinPath):
        """ Add proteins from proteinPath to the database specified """
        # self.connection = sqlite3.connect(self.filename)
        self.insertProteins(proteinPath, True)
        self.readRulesFromDB()
        self.insertCoverageInfo(self.proteins, self.rules)
        self.insertItemInfo()
        # self.connection.close()        

    def createFile(self):
        """ Creates a new sqlite file for the database """
        return sqlite3.connect(self.filename)

    def insertProteins(self, proteinPath, update=False):
        """ Insert the proteins into the DB """
        connection = self.createFile()
        cursor = connection.cursor()

        # Create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS protein
             (idProtein INTEGER PRIMARY KEY, filename TEXT, encoding TEXT)''')


        print("Inserting protein info...")
        index = 1
        if update:
            cursor.execute("SELECT MAX(idProtein) FROM protein")
            index = cursor.fetchone()[0] + 1
        
        #Read the proteins and insert them.
        for filename in os.listdir(proteinPath):
            fname = filename.strip()
            fp = FastaParser()
            fp.readFile(proteinPath+fname)
            toInsert = []
            
            for protein in fp.getProteins():
                toInsert.append((index, protein.getEncoding(), fname))
                self.proteins[index] = protein
                index += 1

            cursor.executemany('INSERT INTO protein(idProtein, encoding, filename) VALUES (?,?,?)', toInsert)


        connection.commit()
        connection.close()
    

    def insertRules(self, ruleFile):
        """ Insert the rules into the DB """
        connection = self.createFile()
        cursor = connection.cursor()

        # Create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS rule
             (idRule INTEGER PRIMARY KEY, rule TEXT, antecedent TEXT, consequent TEXT, ruleType INTEGER)''')

        print("Inserting rule info...")
        index = 1
        #Read the rules and insert them.
        with open(ruleFile, 'r') as infile:
            for line in infile:
                rule = Rule(line)
                self.rules[index] = rule
                toInsert = (index, line.strip(), ', '.join(rule.antecedent), rule.consequent, rule.getRuleType())
                cursor.execute('INSERT INTO rule(idRule, rule, antecedent, consequent, ruleType) VALUES (?,?,?,?,?)', toInsert)
                index += 1

        connection.commit()
        connection.close()



    def insertCoverageInfo(self, proteins, rules):
        """ Insert the coverage info for the proteins/rules. Proteins is a dict or Protein and rules is a dict of Rule """
        connection = self.createFile()
        cursor = connection.cursor()

        # Create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS rule_coverage
             (idRule INTEGER, idProtein INTEGER, fraction REAL, coverageMode INTEGER, consequentOcurrenceType INTEGER, antecedentRepeats TEXT, 
             consequentRepeats TEXT, consequentRepeatsDistances TEXT, consequentAvgRepeatDistance REAL, antecedentRepeatsDistances TEXT, antecedentAvgRepeatDistances TEXT)''')

        protein_count = 0
        protein_amount = len(proteins.items())

        connection.commit()
        connection.close()

        print("Inserting coverage info...")

        # TODO: Buscar una mejor forma de dividir el diccionario "proteins"
        # Aca divido el diccionario en N listas de tuplas para apliar paralelismo
        curr_bucket = 0
        # TODO: parametrizar
        num_buckets = 4 # Amount of processes
        proteins_items_list = [[] for _ in range(num_buckets)]

        for idProtein, protein in proteins.items():
            proteins_items_list[curr_bucket].append((idProtein, protein))
            curr_bucket = (curr_bucket + 1) % num_buckets

        rules_and_proteins_items_list = [ [process_num, protein_list, rules, self.filename] for process_num, protein_list in enumerate(proteins_items_list) ]

        with Pool(processes=num_buckets) as pool:
            insert_values_proceses = pool.map(lambda ps: insert_coverage_info_of_proteins(*ps), rules_and_proteins_items_list)

        connection = self.createFile()
        cursor = connection.cursor()

        for insert_values in insert_values_proceses:
            for toinsert in insert_values:
                cursor.execute('''INSERT INTO rule_coverage(idRule, idProtein, fraction, coverageMode, consequentOcurrenceType, antecedentRepeats,
                    consequentRepeats, consequentRepeatsDistances, consequentAvgRepeatDistance, antecedentRepeatsDistances, antecedentAvgRepeatDistances)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)''', toinsert)

        connection.commit()
        connection.close()


    def insertItemInfo(self):
        """ Add item data to the item table stats """
        print("Inserting item info...")
        rs = RuleStats(self.filename)
        connection = self.createFile()
        cursor = connection.cursor()

        # Create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS item
             (idItem INTEGER, item TEXT, itemFunction INTEGER, qtyRepeats INTEGER, avgDistance REAL, qtyProteins INTEGER)''')

        consequents = {}
        antecedents = {}

        for row in self.getRuleCoverageIterator():
            idProtein = row[1]
            protein = row[2]
            ruleStr = row[3]
            rule = Rule(ruleStr)

            if rule.consequent not in consequents:
                consequents[rule.consequent] = {"itemFunction": RuleStats.CONSEQUENT, "qtyRepeats":0, "avgDistances":[], "qtyProteins":set()}

            repeats = rs.getOcurrencesIndexes(rule.consequent, protein)
            consequents[rule.consequent]["qtyRepeats"] = consequents[rule.consequent]["qtyRepeats"] + len(repeats)
            consequents[rule.consequent]["qtyProteins"].add(idProtein)
            if len(repeats) > 1:
                distancesBetweenConsecutiveRepeats = rs.distanceBetweenConsecutiveRepeats(rule.consequent, protein)
                if len(distancesBetweenConsecutiveRepeats) > 0:
                    avgRepeatDistance = rs.averageOcurrence(distancesBetweenConsecutiveRepeats)
                    consequents[rule.consequent]["avgDistances"].append(avgRepeatDistance)


            for ant in rule.antecedent:
                if ant not in antecedents:
                    antecedents[ant] = {"itemFunction": RuleStats.ANTECEDENT, "qtyRepeats":0, "avgDistances":[], "qtyProteins":set()}

                repeats = rs.getOcurrencesIndexes(ant, protein)
                antecedents[ant]["qtyRepeats"] = antecedents[ant]["qtyRepeats"] + len(repeats)
                antecedents[ant]["qtyProteins"].add(idProtein)
                if len(repeats) > 1:
                    distancesBetweenConsecutiveRepeats = rs.distanceBetweenConsecutiveRepeats(ant, protein)
                    if len(distancesBetweenConsecutiveRepeats) > 0:
                        avgRepeatDistance = rs.averageOcurrence(distancesBetweenConsecutiveRepeats)
                        antecedents[ant]["avgDistances"].append(avgRepeatDistance)


        stmt = '''INSERT INTO item (idItem, item, itemFunction, qtyRepeats, avgDistance, qtyProteins) 
            values (?,?,?,?,?,?)
            '''

        idItem = 1
        for item, data in antecedents.items():
            values = (idItem, item, data["itemFunction"], data["qtyRepeats"], rs.averageOcurrence(data['avgDistances']), len(data["qtyProteins"]))
            cursor.execute(stmt, values)
            idItem = idItem + 1

        for item, data in consequents.items():
            values = (idItem, item, data["itemFunction"], data["qtyRepeats"], rs.averageOcurrence(data['avgDistances']), len(data["qtyProteins"]))
            idItem = idItem + 1
            cursor.execute(stmt, values)

        connection.commit()
        connection.close()


    def getRuleCoverageIterator(self):
        """ Returns an iterable to the rule coverage table joined with the relevant fields in order to query the stat for rules/items """
        connection = self.createFile()
        res = connection.cursor().execute('''SELECT rc.idRule, rc.idProtein, p.encoding as protein, r.rule as rule FROM rule_coverage rc
            INNER JOIN protein p on p.idProtein = rc.idProtein
            INNER JOIN rule r on r.idRule = rc.idRule
            ''')
        # connection.close()
        return res

    def addStatsToRuleCoverage(self):
        """ Adds stats to the coverage database """
        connection = self.createFile()
        updateCursor = connection.cursor()
        for row in self.getRuleCoverageIterator():

            idRule = row[0]
            idProtein = row[1]
            protein = row[2]
            ruleStr = row[3]

            rule = Rule(ruleStr)
            #self.printDebugInfo(rule, protein)

            modifyStmt = '''UPDATE rule_coverage 
                SET consequentOcurrenceType = ?, 
                    antecedentRepeats = ?,
                    consequentRepeats = ?,
                    consequentRepeatsDistances = ?,
                    consequentAvgRepeatDistance = ?,
                    antecedentRepeatsDistances = ?,
                    antecedentAvgRepeatDistances = ?
                WHERE idRule = ? AND idProtein = ?
                '''

            ocurrenceType = rs.ocurrenceType(rule, protein)
            antecedentRepeats = []
            antecedentRepeatsDistances = []
            antecedentAvgRepeatDistances = []
            consequentRepeats = rs.getOcurrencesIndexes(rule.consequent, protein)
            consequentRepeatsDistances = rs.distanceBetweenConsecutiveRepeats(rule.consequent, protein)
            
            consequentAvgRepeatDistance = rs.averageOcurrence(consequentRepeatsDistances)

            for ant in rule.antecedent:
                antecedentRepeats.append(rs.getOcurrencesIndexes(ant, protein))
                ocurrs = rs.distanceBetweenConsecutiveRepeats(ant, protein)
                antecedentRepeatsDistances.append(ocurrs)
                antecedentAvgRepeatDistances.append(rs.averageOcurrence(ocurrs))


            values = (ocurrenceType, str(antecedentRepeats), str(consequentRepeats), str(consequentRepeatsDistances), consequentAvgRepeatDistance, str(antecedentRepeatsDistances), str(antecedentAvgRepeatDistances), idRule, idProtein)
            updateCursor.execute(modifyStmt, values)

        connection.commit()
        connection.close()


    def readRulesFromDB(self):
        """ Read the rules into the DB """
        print("Loading rules from DB...")
        connection = self.createFile()
        cursor = connection.cursor()

        #Read the rules from the DB.
        for row in cursor.execute('''SELECT * FROM rule'''):
            rule = Rule(row[1])                
            self.rules[row[0]] = rule

        connection.close()
            
def parameterNotSet(param):
    """ Returns whether the parameter param is set """
    return param is None or len(param) == 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proteinPath", help="The path that contains the proteins to be analized", type=str)
    parser.add_argument("--ruleFile", help="The file with the rules to check for coverage against the proteins", type=str)
    parser.add_argument('--add', help="Add rules/proteins to the existing sqlite file", type=bool)
    parser.add_argument('--filename', help="Filename for the SQLite database", type=str, default="protein-rules.db")

    args = parser.parse_args()

    if parameterNotSet(args.proteinPath):
        print("ERROR: proteinPath required and not set!! - Exiting...")
        sys.exit(-1)

    rc = GenerateProteinRuleDb(args.filename)
    if args.add:
        rc.addProteins(args.proteinPath)
    else:
        rc.createDB(args.proteinPath, args.ruleFile)


if __name__ == "__main__":
    # execute only if run as a script
    main()