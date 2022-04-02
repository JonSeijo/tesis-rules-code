# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import argparse
import re
from pathlib import Path
from fastaread import Protein,FastaParser
from rulegroup import RuleGroupParser,Rule
from base_graph import GraphvizGraph
from rulecoverage import RuleCoverage, RuleCoverageResult

class RuleGraph(object):
    """ Generates a graph based on how rules are related to each other by implications between
    antecedents and consequents. Generates a dot file that is later turned into a png image of the graph
    via dotviz. """

    def __init__(self, ruleFile, proteinPath, threshold = 1, highlightIkba = False):
        """ Initialize object and set parameters """
        super(RuleGraph, self).__init__()
        self.adjacencyList = {}
        self.adjacencyListHighlight = {}
        self.ruleFile = ruleFile
        self.proteinPath = proteinPath
        self.proteins = []
        self.highlightIkba = highlightIkba
        self.grapher = GraphvizGraph("implication.dot", "implication.png", "digraph", "Grafo de implicaciones entre MRs integrantes de reglas.", threshold)

    def readRules(self):
        """ Parse the rule file. Highlighting ikba. Generate the adjacency list of the
        rule implication graph """
        encoding = ("MFQAAERPQEWAMEGPRDGLKKERLLDDRHD"
            "GLDSMKDEEYEQMVKELQEIRLEPQEVPRGSEPWKQQLTEDGDSFLHLAI"
            "IHEEKALTMEVIRQVKGDLAFLNFQNNLQQTPLHLAVITNQPEIAEALLGAGCDPELRDFRGNTPLHLACEQGC"
            "LASVGVLTQSCTTPHLHSILKATNYNGHTCLHLASIHGYLGIVELLVSLGADVNAQEPCNGRTA"
            "LHLAVDLQNPDLVSLLLKCGADVNRVTYQGYSPYQLTWGRPSTRIQQQLGQLTLENLQMLPESE"
            "DEESYDTESEFTEFTEDELPYDDCVFGGQRLTL")
        ikba = Protein(encoding, 'comment', '')

        qtyRules = 0
        with open(self.ruleFile, 'r') as infile:
            for line in infile:
                rule = Rule(line)
                qtyRules += 1
                
                ruleCoversIkba = False
                if self.highlightIkba:
                    cov = RuleCoverage("","","test.txt","vector")
                    ruleCoversIkba = cov.getCoverageOfRuleForProtein(ikba, rule).isProteinCovered()
                    #print(rule.ruleRaw)
                                
                for antecedent in rule.antecedent:
                    self.grapher.addLink(antecedent, rule.consequent, {'highlight':ruleCoversIkba, 'edgeValue': str(self.frequencyInProteins(antecedent,rule.consequent))})

        print("Read %s components from %s rules." % (str(len(self.adjacencyList)), qtyRules))

    def readProteins(self):
        """ Read the proteins from the path and store them """
        for filename in os.listdir(self.proteinPath):
            fp = FastaParser()
            fp.readFile(self.proteinPath+filename.strip())
            for protein in fp.getProteins():
                self.proteins.append(protein.getEncoding())

        print("Read %s proteins." % (str(len(self.proteins))))


    def frequencyInProteins(self, ant, con):
        """ Compute the frequency in proteins of the consequent and antecedents received """
        antPattern = re.compile(ant, re.IGNORECASE)
        conPattern = re.compile(con, re.IGNORECASE)

        matches = 0
        for protein in self.proteins:
            if antPattern.search(protein) != None and conPattern.search(protein) != None:
                matches += 1

        return round(matches/len(self.proteins), 5)

    def createGraph(self):
        """ Read rules, proteins and then generate the graphfile. After that call the graphviz executable installed in the system """
        self.readProteins()
        self.readRules()
        self.grapher.graph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ruleFile", help="The file with the rules graph")
    parser.add_argument("proteinPath", help="The path that contains the proteins to be analized")
    parser.add_argument("--threshold", help="The minimum number of outgoing edges to consider when making the graph. Below the threshold they won't be considered",
        default=1)
    parser.add_argument("--highlightIkba", help="Whether to highlight edges of rules that cover ikba.", default=False)

    args = parser.parse_args()

    if args.threshold == None:
        args.threshold = 1

    rc = RuleGraph(args.ruleFile, args.proteinPath, int(args.threshold), args.highlightIkba)
    rc.createGraph()
    print("DONE!")

if __name__ == "__main__":
    # execute only if run as a script
    main()