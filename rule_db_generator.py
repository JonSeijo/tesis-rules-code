# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import sys
import argparse
import re
import inspect
from pathlib import Path
from main_code.rulegroup.fastaread import Protein,FastaParser
from main_code.rulegroup.rulegroup import RuleGroupParser,Rule
from main_code.rulegroup.rulecoverage import RuleCoverage
from main_code.rulegroup.rule_stats import RuleStats

from db_controller import DBController

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

                toInsert = {
                    'idRule': idRule, 
                    'idProtein': idProtein, 
                    'fraction': fraction, 
                    'coverageMode': mode, 
                    'consequentOcurrenceType': ocurrenceType, 
                    'antecedentRepeats': str(antecedentRepeats), 
                    'consequentRepeats': str(consequentRepeats), 
                    'consequentRepeatsDistances': str(consequentRepeatsDistances), 
                    'consequentAvgRepeatDistance': consequentAvgRepeatDistance, 
                    'antecedentRepeatsDistances': str(antecedentRepeatsDistances), 
                    'antecedentAvgRepeatDistances': str(antecedentAvgRepeatDistances)
                }

                toinsert_values.append(toInsert)

    return toinsert_values




class GenerateProteinRuleDb(object):
    """docstring for GenerateProteinRuleDb"""
    def __init__(self, nthreads, filename="protein-rules.db"):
        super(GenerateProteinRuleDb, self).__init__()

        self.proteins = {}
        self.rules = {}
        self.filename = filename
        self.nthreads = nthreads

        self.db_controller = DBController(self.filename)


    def createDB(self, proteinPath, ruleFile):
        """ Create a DB from scratch """
        self.insert_proteins(proteinPath)
        self.insert_rules_and_metadata(ruleFile)

        self.load_rules_from_db() 

        self.insert_coverage_info(self.proteins, self.rules)
        self.insert_item_info()

    def addProteins(self, proteinPath):
        """ Add proteins from proteinPath to the database specified """
        self.insert_proteins(proteinPath, True)
        self.load_rules_from_db()
        self.insert_coverage_info(self.proteins, self.rules)
        self.insert_item_info()

    def create_tables(self):
        self.db_controller.create_tables()

    def insert_proteins(self, proteinPath, update=False):
        print("Inserting protein info...")

        index = 1
        if update:
            last_protein_id = self.db_controller.get_last_protein_id()
            index = last_protein_id + 1
        
        #Read the proteins and insert them.
        for filename in os.listdir(proteinPath):
            fname = filename.strip()
            fp = FastaParser()
            fp.readFile(proteinPath+fname)
            proteins_to_insert = []
            
            for protein in fp.getProteins():
                proteins_to_insert.append({
                    'idProtein': index,
                    'encoding': protein.getEncoding(),
                    'filename': fname
                })

                self.proteins[index] = protein
                index += 1

            self.db_controller.insert_proteins(proteins_to_insert)


    def insert_rules_and_metadata(self, rule_filename):
        """ Insert the rules into the DB """
        rules_df = info_rules.build_df_rules_from_path(rule_filename)
        metadata = info_rules.build_rule_metadata_from_rule_filename(rule_filename)

        metadata_id = self.insert_rule_metadata(metadata, rule_filename)
        self.insert_rules(rules_df, metadata_id)


    # TODO: "filename_rules" deberia ser parte de la metadata
    # TODO: metadata deberia tener un .to_dict() y resolverlo?
    def insert_rule_metadata(self, metadata, filename_rules):
        print("- Inserting rules metadata")

        rule_metadata_to_insert = {
            'rules_filename': filename_rules,
            'family': metadata.family,
            'min_len': metadata.min_len,
            'transaction_type': metadata.transaction_type,
            'maximal_repeat_type': metadata.mr_type,
            'clean_mode': metadata.clean_mode,
            'min_support': metadata.min_support,
            'min_confidence': metadata.min_confidence
        }

        rule_metadata_last_id = self.db_controller.insert_rule_metadata(rule_metadata_to_insert)
        return rule_metadata_last_id

    def insert_rules(self, rules_df, metadata_id):
        print("- Inserting rules data")
        rules_to_insert = []
        for index, rr in rules_df.iterrows():
            rule_to_insert = {
                'rule': rr['rules'],
                'antecedent': rr['antecedent'],
                'consequent': rr['consequent'],
                'rule_type': rr['ruletype'],
                'rule_type_simple': rr['ruletype_simple'],
                'rule_size': rr['rule_size'],
                'count': rr['count'],
                'support': rr['support'],
                'confidence': rr['confidence'],
                'lift': rr['lift'],
                'id_rule_metadata': metadata_id
            }

            rules_to_insert.append(rule_to_insert)

        self.db_controller.insert_rules(rules_to_insert)


    def insert_coverage_info(self, proteins, rules):
        """ Insert the coverage info for the proteins/rules. Proteins is a dict or Protein and rules is a dict of Rule """

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

        for insert_values in insert_values_proceses:
            self.db_controller.insert_rule_coverage_values(insert_values)


    def insert_item_info(self):
        """ Add item data to the item table stats """
        print("Inserting item info...")
        rs = RuleStats(self.filename)
        consequents = {}
        antecedents = {}

        for row in self.db_controller.get_rule_coverage_iterator():
            idProtein = row['idProtein']
            protein = row['protein']
            ruleStr = row['ruleStr']

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


        idItem = 1

        for items in [antecedents.items(), consequents.items()]:
            items_to_insert = []
            for item, data in items:
                items_to_insert.append({
                    'idItem': idItem,
                    'item': item,
                    'itemFunction': data["itemFunction"],
                    'qtyRepeats': data["qtyRepeats"],
                    'avgDistance': rs.averageOcurrence(data['avgDistances']),
                    'qtyProteins': len(data["qtyProteins"])
                })
                idItem = idItem + 1

            self.db_controller.insert_items(items_to_insert)


    def addStatsToRuleCoverage(self):
        """ Adds stats to the coverage database """
        for row in self.db_controller.get_rule_coverage_iterator():

            idRule = row['idRule']
            idProtein = row['idProtein']
            protein = row['protein']
            ruleStr = row['ruleStr']

            rule = Rule(ruleStr)

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

            values = {
                'idRule': idRule,
                'idProtein': idProtein,
                'consequentOcurrenceType': ocurrenceType,
                'antecedentRepeats': str(antecedentRepeats),
                'consequentRepeats': str(consequentRepeats),
                'consequentRepeatsDistances': str(consequentRepeatsDistances),
                'consequentAvgRepeatDistance': consequentAvgRepeatDistance,
                'antecedentRepeatsDistances': str(antecedentRepeatsDistances),
                'antecedentAvgRepeatDistances': str(antecedentAvgRepeatDistances),
            }

            self.db_controller.update_rule_coverage(rule_coverage_to_update, idRule, idProtein)



    def load_rules_from_db(self):
        """ Read the rules into the DB """
        print("Loading rules from DB...")

        #Read the rules from the DB.
        for row in self.db_controller.get_rules():
            rule = Rule(row['rule'])                
            self.rules[row['idRule']] = rule

            
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