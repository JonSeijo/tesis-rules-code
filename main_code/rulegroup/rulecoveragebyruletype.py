# -*- coding: utf-8 -*-
#!/usr/bin/python

import itertools
import os
import argparse
from pathlib import Path
from rulecoverageexport import RuleCoverageExportToImage,RuleCoverageExportToVector, RuleCoverageExportToXYZ, RuleCoverageExportToHtml, RuleCoverageExportToCsv, RuleByTypeCoverageExportToImage
from rulecoverage import RuleCoverage
from rulegroup import RuleGroupParser,Rule
from fastaread import Protein,FastaParser



class RuleCoverageByRuleType(RuleCoverage):
    """ Performs the coverage operations for a set of rules against a set of proteins by rule type """

    OVERLAPPING = 1
    ADDS_INFO = 2
    OTHER = 3

    def exportType(self, exportType):
        """ Defines the export types available """

        exportTypes = {
            'image': RuleByTypeCoverageExportToImage(self.coverageFile)
        }

        return exportTypes[str(exportType)]

    def openRules(self):
        """ Open & parse the rules from the specified rule file but group them by type """

        ruleQty = 0
        rules = {self.OVERLAPPING: [], self.ADDS_INFO:[], self.OTHER: []}
        with open(self.ruleFile, 'r') as infile:
            for line in infile:
                ruleQty += 1
                r = Rule(line)
                rules[r.getRuleType()].append(r)

        #print("Read %d rules as:  %d | %d | %d" % (ruleQty, len(rules[1]), len(rules[2]), len(rules[3]) ))
        return rules

    def process(self):
        """ Read the rules and store them. Then read the protein index file and compute the coverage
        for the rules against the protein. Store the result in the selected output option """
        
        ruleFileExtraData = {'total':0, 'covered':0} #Set extra parametrs for showing summary of coverage
        rootFolder = os.path.dirname(os.path.realpath(self.proteinFile)) + os.path.sep
        
        #Read the rules from the rulefile.
        rules = self.openRules()
        ruleTypes = [self.OVERLAPPING, self.ADDS_INFO, self.OTHER]

        index = 0
        fp = FastaParser()
        #Read each protein
        with open(self.proteinFile, 'r') as pfile:
            for line in pfile:
                fp.readFile(line.strip())
                for protein in fp.getProteins():
                    for t in ruleTypes:
                        resultVector = self.getCoverageOfRulesForProtein(protein, rules[t]).getResultVector()
                        self.export.addData(resultVector, index, protein.getEncoding(), self.clearPath(protein.getFilename()), None, t)
                    
                    index += 1 
                    self.export.addExtraSeparation()
                    print("Coverage for protein %s...\n", str(index))

        self.export.export()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("proteinFile", help="The file that contains the proteins to be analized")
    parser.add_argument("ruleFile", help="The file with the rules to check for coverage against the proteins")
    parser.add_argument("coverageFile", help="The coverage file to where to output the coverage results")
    parser.add_argument("exportType", help="The way in which to export the results. Options are: image", 
        default='image')
    parser.add_argument("--onlyCovered", help="To consider or not only covered rules", 
        default=False, type=bool)

    args = parser.parse_args()

    rc = RuleCoverageByRuleType(args.proteinFile, args.ruleFile, args.coverageFile, args.exportType, args.onlyCovered)
    rc.process()
    print("DONE!")

if __name__ == "__main__":
    # execute only if run as a script
    main()