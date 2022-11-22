# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import sys
import argparse
import re
import inspect
import ntpath
from pathlib import Path
from main_code.rulegroup.fastaread import Protein,FastaParser
from main_code.rulegroup.rulegroup import RuleGroupParser,Rule
from main_code.rulegroup.rulecoverage import RuleCoverage
from main_code.rulegroup.rule_stats import RuleStats
import sqlite3

from pathos.multiprocessing import ProcessingPool as Pool

# TODO: Arreglar esto de los imports relativos
import info_rules


def insert_coverage_info_of_proteins(process_num, proteins, rules, dbfilename):
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
    def __init__(self, nthreads, filename="protein-rules.db"):
        super(GenerateProteinRuleDb, self).__init__()
        self.proteins = {}
        self.rules = {}
        self.filename = filename
        self.nthreads = nthreads

    def create_tables(self):
        connection = self.create_connection()
        cursor = connection.cursor()

        # Create table 'protein'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS protein
            (idProtein INTEGER PRIMARY KEY, 
            filename TEXT, 
            encoding TEXT)''')


        # Create table 'rule'

        # TODO: Borrar tabla vieja
        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS rule
        #     (idRule INTEGER PRIMARY KEY, 
        #     rule TEXT, 
        #     antecedent TEXT, 
        #     consequent TEXT, 
        #     ruleType INTEGER)''')
        
        # FIXME: id_rule
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule
            (idRule INTEGER PRIMARY KEY,  
            rule TEXT,
            antecedent TEXT,
            consequent TEXT,
            rule_type TEXT,
            rule_type_simple TEXT,
            rule_size INTEGER,
            count INTEGER,
            support REAL,
            confidence REAL,
            lift REAL,
            id_rule_metadata INTEGER)''')


        # 'maximalRepeatType': ALL, NE, NN ..
        # Create table 'rule_metadata'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule_metadata
            (id_rule_metadata INTEGER PRIMARY KEY,
            rules_filename TEXT UNIQUE,
            family TEXT,
            min_len TEXT,
            transaction_type TEXT,
            maximal_repeat_type TEXT,
            clean_mode TEXT,
            min_support TEXT,
            min_confidence TEXT)''')

        # Create table 'rule_coverage'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule_coverage
            (idRule INTEGER, 
            idProtein INTEGER, 
            fraction REAL, 
            coverageMode INTEGER, 
            consequentOcurrenceType INTEGER, 
            antecedentRepeats TEXT, 
            consequentRepeats TEXT, 
            consequentRepeatsDistances TEXT, 
            consequentAvgRepeatDistance REAL, 
            antecedentRepeatsDistances TEXT, 
            antecedentAvgRepeatDistances TEXT)''')

        # Create table 'item'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item
            (idItem INTEGER, 
            item TEXT, 
            itemFunction INTEGER, 
            qtyRepeats INTEGER, 
            avgDistance REAL, 
            qtyProteins INTEGER)''')

        connection.commit()
        connection.close()

    def createDB(self, proteinPath, ruleFile):
        """ Create a DB from scratch """
        self.insertProteins(proteinPath)
        self.insertRules(ruleFile)

        # WIP
        self.readRulesFromDB() 

        self.insertCoverageInfo(self.proteins, self.rules)
        self.insertItemInfo()

    def addProteins(self, proteinPath):
        """ Add proteins from proteinPath to the database specified """
        self.insertProteins(proteinPath, True)
        self.readRulesFromDB()
        self.insertCoverageInfo(self.proteins, self.rules)
        self.insertItemInfo()

    def create_connection(self):
        """ Creates a new sqlite file for the database """
        return sqlite3.connect(self.filename)

    def insertProteins(self, proteinPath, update=False):
        """ Insert the proteins into the DB """
        connection = self.create_connection()
        cursor = connection.cursor()

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

        connection = self.create_connection()

        # WIP: Este sería el metodo nuevo....
        # ... el problema es que necesito obtener el index de insersion y la rule info para lo de converage
        # ... la solucion que se me ocurre es en lo de coverage cargarlo de la db y ya? 
        # ... a ver si se puede hacer eso ...
        # ... deberia estar funcoinando (para el add protein) con lo de readFromDB
        # ... pasa que ahora cambie la tabla y la info, aver...

        rules_df = info_rules.build_df_rules_from_path(ruleFile)
        metadata = info_rules.build_rule_metadata_from_rule_filename(ruleFile)

        metadata_id = self.insert_rule_metadata(connection, metadata, ruleFile)

        self.insert_rules(connection, rules_df, metadata_id)
        connection.close()



        # cursor = connection.cursor()

        # print("Inserting rule info...")
        # index = 1
        # #Read the rules and insert them.
        # with open(ruleFile, 'r') as infile:
        #     for line in infile:
        #         rule = Rule(line)
        #         self.rules[index] = rule
        #         toInsert = (index, line.strip(), ', '.join(rule.antecedent), rule.consequent, rule.getRuleType())
        #         cursor.execute('INSERT INTO rule(idRule, rule, antecedent, consequent, ruleType) VALUES (?,?,?,?,?)', toInsert)
        #         index += 1

        # connection.commit()
        # connection.close()

    def insert_rule_metadata(self, connection, metadata, filename_rules):
        
        print("- Inserting rules metadata")
        
        # rule_metadata = (filename_rules, family, 
        #     min_support, min_confidence, min_len, mr_type)
        
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO rule_metadata( 
                rules_filename,
                family,
                min_len,
                transaction_type,
                maximal_repeat_type,
                clean_mode,
                min_support,
                min_confidence)
            VALUES (?,?,?,?,?,?,?,?)''', (
                filename_rules, metadata.family, metadata.min_len, metadata.transaction_type,
                metadata.mr_type, metadata.clean_mode, metadata.min_support, metadata.min_confidence))

        rule_metadata_id = cursor.lastrowid
        
        connection.commit()

        return rule_metadata_id

    # TODO: Podria haber usado algo como pandas.DataFrame.to_sql? Si
    def insert_rules(self, connection, rules_df, metadata_id):
        print("- Inserting rules data")
        cursor = connection.cursor()

        for index, rr in rules_df.iterrows():

            rule_to_insert = (
                rr['rules'],
                rr['antecedent'],
                rr['consequent'],
                rr['ruletype'],
                rr['ruletype_simple'],
                rr['rule_size'],
                rr['count'],
                rr['support'],
                rr['confidence'],
                rr['lift'],
                metadata_id
            )

            cursor.execute('''
                INSERT INTO rule(
                    rule,
                    antecedent,
                    consequent,
                    rule_type,
                    rule_type_simple,
                    rule_size,
                    count,
                    support,
                    confidence,
                    lift,
                    id_rule_metadata)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)''', rule_to_insert)

        connection.commit()



    def insertCoverageInfo(self, proteins, rules):
        """ Insert the coverage info for the proteins/rules. Proteins is a dict or Protein and rules is a dict of Rule """
        connection = self.create_connection()
        cursor = connection.cursor()

        protein_count = 0
        protein_amount = len(proteins.items())

        connection.commit()
        connection.close()

        print("Inserting coverage info...")

        # TODO: Buscar una mejor forma de dividir el diccionario "proteins"
        # Aca divido el diccionario en N listas de tuplas para apliar paralelismo
        curr_bucket = 0

        num_buckets = self.nthreads # Amount of processes
        proteins_items_list = [[] for _ in range(num_buckets)]

        for idProtein, protein in proteins.items():
            proteins_items_list[curr_bucket].append((idProtein, protein))
            curr_bucket = (curr_bucket + 1) % num_buckets

        rules_and_proteins_items_list = [ [process_num, protein_list, rules, self.filename] for process_num, protein_list in enumerate(proteins_items_list) ]

        with Pool(processes=num_buckets) as pool:
            insert_values_proceses = pool.map(lambda ps: insert_coverage_info_of_proteins(*ps), rules_and_proteins_items_list)

        connection = self.create_connection()
        cursor = connection.cursor()

        for insert_values in insert_values_proceses:
            cursor.executemany('''INSERT INTO rule_coverage(idRule, idProtein, fraction, coverageMode, consequentOcurrenceType, antecedentRepeats,
                consequentRepeats, consequentRepeatsDistances, consequentAvgRepeatDistance, antecedentRepeatsDistances, antecedentAvgRepeatDistances)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)''', insert_values)

        connection.commit()
        connection.close()


    def insertItemInfo(self):
        """ Add item data to the item table stats """
        print("Inserting item info...")
        rs = RuleStats(self.filename)
        connection = self.create_connection()
        cursor = connection.cursor()

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
        connection = self.create_connection()
        res = connection.cursor().execute('''SELECT rc.idRule, rc.idProtein, p.encoding as protein, r.rule as rule FROM rule_coverage rc
            INNER JOIN protein p on p.idProtein = rc.idProtein
            INNER JOIN rule r on r.idRule = rc.idRule
            ''')
        # connection.close()
        return res

    def addStatsToRuleCoverage(self):
        """ Adds stats to the coverage database """
        connection = self.create_connection()
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
        connection = self.create_connection()
        cursor = connection.cursor()

        # TODO: El tema es que usa el simplified_rules ....
        # Ver cual seria la diferencia

        #Read the rules from the DB.
        for row in cursor.execute('''SELECT * FROM rule'''):

            # TODO: Esto anda de casualidad, porque 'rule' es la columna 1. Revisar select!
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
    parser.add_argument('--threads', help="Amount of threads", type=int, default=4)
    args = parser.parse_args()

    if parameterNotSet(args.proteinPath):
        print("ERROR: proteinPath required and not set!! - Exiting...")
        sys.exit(-1)

    print("================================================")
    print("Running rule_db_generator with arguments:")
    print()
    print("proteinPath:", args.proteinPath)
    print("ruleFile:   ", args.ruleFile)
    print("add:        ", args.add)
    print("filename:   ", args.filename)
    print("threads:    ", args.threads)
    print("================================================")

    rc = GenerateProteinRuleDb(args.threads, args.filename)
    rc.create_tables()
    if args.add:
        rc.addProteins(args.proteinPath)
    else:
        rc.createDB(args.proteinPath, args.ruleFile)


if __name__ == "__main__":
    # execute only if run as a script
    main()