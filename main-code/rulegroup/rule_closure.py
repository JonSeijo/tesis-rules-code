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
import sqlite3

class RuleClosureFromDb(object):
    """ Compute the transitive closure form a set of rules and proteins by reading data from a SQLite file """
    def __init__(self, filename="protein-rules.db"):
        super(RuleClosureFromDb, self).__init__()
        self.output = "rule-closure.txt"
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()


    def readRulesFromDB(self):
        """ Read the rules into the DB """
        self.rules = {}
        self.rulesToCheck = set()

        #Read the rules from the DB.
        for row in self.cursor.execute('''SELECT idRule, rule FROM rule'''):
            rule = Rule(row[1])                
            self.rules[row[0]] = rule
            self.rulesToCheck.add(row[0])

    def getProteinsOfRule(self, ruleId):
        """ Get the proteins covered by a given rule """
        proteinIds = set()
        for row in self.cursor.execute('''SELECT idProtein FROM rule_coverage where idRule = ?''', (ruleId,)):
            proteinIds.add(row[0])

        return proteinIds

    def getRulesOfProtein(self, proteinId):
        """ Get the rules that cover a given protein """
        ruleIds = set()
        for row in self.cursor.execute('''SELECT idRule FROM rule_coverage WHERE idProtein = ?''', (proteinId,)):
            ruleIds.add(row[0])

        return ruleIds

    def addRuleToGroup(self, rule, group):
        """ Add rule to group of rules """
        if group not in self.groups:
            self.groups[group] = set()

        self.groups[group].add(rule)

    def transitiveClosure(self):
        """ Compute the transitive closure of the group of rules """
        self.readRulesFromDB()
        self.groups = {}
        groupIndex = 0

        print("Got %s rules to check" % str(len(self.rulesToCheck)))

        while len(self.rulesToCheck) > 0:
            rule = self.rulesToCheck.pop()
            for proteinIdToCheck in self.getProteinsOfRule(rule):
                for ruleIdOfProtein in self.getRulesOfProtein(proteinIdToCheck):
                    self.addRuleToGroup(ruleIdOfProtein, groupIndex)
                    if ruleIdOfProtein in self.rulesToCheck:
                        self.rulesToCheck.remove(ruleIdOfProtein)
            groupIndex = groupIndex + 1

    def printRules(self):
        """ Write groups to file computed from the closure """
        outfile = open(self.output, 'w')
        for group, ruleSet in self.groups.items():
            outfile.write("Group %s\n" % str(group))
            for rule in ruleSet:
                outfile.write(self.rules[rule].ruleRaw+"\n")

        outfile.close()

def parameterNotSet(param):
    """ Returns whether the parameter param is set """
    return param is None or len(param) == 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help="Filename for the SQLite database", type=str, default="protein-rules.db")

    args = parser.parse_args()

    if parameterNotSet(args.filename):
        print("ERROR: filename for the database required and not set!! - Exiting...")
        sys.exit(-1)

    rc = RuleClosureFromDb(args.filename)
    rc.transitiveClosure()
    rc.printRules()


if __name__ == "__main__":
    # execute only if run as a script
    main()