# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import sys
import argparse
import re
import inspect
from pathlib import Path
from main_code.rulegroup.fastaread import Protein, FastaParser
from main_code.rulegroup.rulegroup import RuleGroupParser,Rule
from main_code.rulegroup.rulecoverage import RuleCoverage
from main_code.rulegroup.rule_stats import RuleStats

from db_controller import DBController

from pathos.multiprocessing import ProcessingPool as Pool

# TODO: Arreglar esto de los imports relativos
import info_rules


def insert_coverage_info_of_proteins(process_num, proteins, rules, dbfilename):
    """
    proteins: Dict[idProtein, Protein]
    rules: Dict[idRule, Rule]
    """
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

                to_insert = {
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

                toinsert_values.append(to_insert)

    return toinsert_values




class GenerateProteinRuleDb(object):
    """docstring for GenerateProteinRuleDb"""
    def __init__(self, nthreads, db_filename="protein-rules.db"):
        super(GenerateProteinRuleDb, self).__init__()

        self.proteins = {}
        self.rules = {}
        self.db_filename = db_filename
        self.nthreads = nthreads

        self.db_controller = DBController(self.db_filename)
        self.create_tables()


    def update_db(self, protein_path, rule_filename):
        rule_metadata = info_rules.build_rule_metadata_from_rule_filename(rule_filename)

        self.insert_and_load_proteins(protein_path, rule_metadata.family)
        self.insert_rules_and_metadata(rule_filename, rule_metadata)

        self.load_rules_from_db() 
        self.insert_coverage_info()
        self.insert_item_info()

    def create_tables(self):
        self.db_controller.create_tables()


    def insert_and_load_proteins(self, path_protein, family):
        print("insert_and_load_proteins...")
        print("path_protein", path_protein)
        print("family", family)

        # if family exists in protein db, only load them
        db_proteins = self.db_controller.get_proteins_of_family(family)

        print(f"Encontre {len(db_proteins)} proteinas de esa familia...")

        if len(db_proteins) > 0:
            print("!! Protein family already exists !!")
            print(" Loading existing protein family...")
            for db_protein in db_proteins:
                self.proteins[db_protein['idProtein']] = Protein(
                    db_protein['encoding'], '', db_protein['filename'])

            return

        else:
            print("Loading and inserting proteins from .fasta files")
            last_protein_id = self.db_controller.get_last_protein_id()

            index = last_protein_id + 1

            #Read the fasta proteins from files, insert them and load them.
            for filename_fasta in os.listdir(path_protein):
                fname = filename_fasta.strip()
                fp = FastaParser()
                fp.readFile(os.path.join(path_protein, fname))

                proteins_to_insert = []
                for protein in fp.getProteins():
                    proteins_to_insert.append({
                        'idProtein': index,
                        'family': family,
                        'encoding': protein.getEncoding(),
                        'filename': fname
                    })

                    self.proteins[index] = protein
                    index += 1

                self.db_controller.insert_proteins(proteins_to_insert)


    def insert_rules_and_metadata(self, rule_filename, metadata):
        """ Insert the rules into the DB """
        rules_df = info_rules.build_df_rules_from_path(rule_filename)

        metadata_id = self.insert_rule_metadata(metadata)
        self.insert_rules(rules_df, metadata_id)


    # TODO: metadata deberia tener un .to_dict() y resolverlo?
    def insert_rule_metadata(self, metadata):
        print("- Inserting rules metadata")

        rule_metadata_to_insert = {
            'rules_filename': metadata.rules_filename,
            'family': metadata.family,
            'min_len': metadata.min_len,
            'transaction_type': metadata.transaction_type,
            'maximal_repeat_type': metadata.maximal_repeat_type,
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


    def insert_coverage_info(self):
        """ Insert the coverage info for the proteins/rules. 
        self.proteins is a dict of Protein and self.rules is a dict of Rule """

        if len(self.proteins) == 0 or len(self.rules) == 0:
            raise Exception("No proteins or rules loaded before calling insert_coverage_info")

        print("Inserting coverage info...")

        # TODO: Buscar una mejor forma de dividir el diccionario "proteins"
        # Aca divido el diccionario en N listas de tuplas para apliar paralelismo
        curr_bucket = 0

        num_buckets = self.nthreads # Amount of processes
        proteins_items_list = [[] for _ in range(num_buckets)]

        for idProtein, protein in self.proteins.items():
            proteins_items_list[curr_bucket].append((idProtein, protein))
            curr_bucket = (curr_bucket + 1) % num_buckets

        rules_and_proteins_items_list = [ 
            [process_num, protein_list, self.rules, self.db_filename] 
            for process_num, protein_list in enumerate(proteins_items_list) 
        ]

        with Pool(processes=num_buckets) as pool:
            insert_values_proceses = pool.map(lambda ps: insert_coverage_info_of_proteins(*ps), rules_and_proteins_items_list)

        for insert_values in insert_values_proceses:
            self.db_controller.insert_rule_coverage_values(insert_values)


    def insert_item_info(self):
        """ Add item data to the item table stats """
        print("Inserting item info...")
        rs = RuleStats(self.db_filename)
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


    # TODO: Borrar? Esto no se usa, para que estaba?
    def updateRuleCoverageStats(self):
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

            
def parameter_not_set(param):
    """ Returns whether the parameter param is set """
    return param is None or len(param) == 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proteinPath", help="The path that contains the proteins to be analized", type=str)
    parser.add_argument("--ruleFile", help="The file with the rules to check for coverage against the proteins", type=str)
    parser.add_argument('--filename', help="Filename for the SQLite database", type=str, default="protein-rules.db")
    parser.add_argument('--threads', help="Amount of threads", type=int, default=4)
    args = parser.parse_args()

    if parameter_not_set(args.proteinPath):
        print("ERROR: proteinPath required and not set!! - Exiting...")
        sys.exit(-1)

    if parameter_not_set(args.ruleFile):
        print("ERROR: ruleFile required and not set!! - Exiting...")
        sys.exit(-1)

    print("================================================")
    print("Running rule_db_generator with arguments:")
    print()
    print("proteinPath:", args.proteinPath)
    print("ruleFile:   ", args.ruleFile)
    print("filename:   ", args.filename)
    print("threads:    ", args.threads)
    print("================================================")

    rc = GenerateProteinRuleDb(args.threads, args.filename)
    
    rc.update_db(args.proteinPath, args.ruleFile)


if __name__ == "__main__":
    # execute only if run as a script
    main()