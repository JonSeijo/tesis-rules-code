# -*- coding: utf-8 -*-
#!/usr/bin/python

import itertools
import os
import argparse
import re
import inspect
import ntpath
from pathlib import Path
from main_code.rulegroup.fastaread import Protein,FastaParser
from main_code.rulegroup.rulegroup import RuleGroupParser,Rule
from main_code.rulegroup.rulecoverageexport import RuleCoverageExportToImage,RuleCoverageExportToVector, RuleCoverageExportToXYZ, RuleCoverageExportToHtml, RuleCoverageExportToCsv

class RuleCoverageResult(object):
    """ Models the result of a protein being covered by a rule """

    MODE_ANTECEDENT = 1
    MODE_CONSEQUENT = 2
    MODE_BOTH = 3

    def __init__(self, antecedentVector, consequentVector, isCovered):
        self.antecedentVector = antecedentVector
        self.consequentVector = consequentVector
        self.isCovered = isCovered
        self.resultVector = [self.antecedentVector[i]+self.consequentVector[i] for i in range(0, len(self.antecedentVector))]

    def isProteinCovered(self):
        """ Return whether the coverage result marks the protein as covered """
        return self.isCovered

    def getConsequentVector(self):
        """ Return only the consequent vector """
        return self.consequentVector

    def getAntecedentVector(self):
        """ Return only the antecedent result """
        return self.antecedentVector

    def getCoverageFraction(self, mode = None):
        """ Returns the coverage fraction from the total ie. values not 0 """
        vector = []
        if mode is None:
            vector = self.resultVector
        elif mode == self.MODE_ANTECEDENT:
            vector = self.antecedentVector
        else:
            vector = self.consequentVector

        return len([k for k in vector if k > 0])/len(vector)

    def getResultVector(self):
        """ Merge the two results """
        return self.resultVector

    
    def mergeVector(self, vector, otherVector):
        """ Merge two result vectors """
        for index in range(0, len(otherVector)):
            if otherVector[index] != vector[index]:
                vector[index] = vector[index] + otherVector[index]
                if vector[index] > 3:
                    vector[index] = 3

        return vector

    def mergeWith(self, otherResult):
        """ Merge the current vector result with the otherResult given as a parameter """       
        if not(isinstance(otherResult, RuleCoverageResult)):
            raise Exception("Invalid merge with non RuleCoverageResult object")

        antecedent = self.mergeVector(self.getAntecedentVector(), otherResult.getAntecedentVector())
        consequent = self.mergeVector(self.getConsequentVector(), otherResult.getConsequentVector())

        result = RuleCoverageResult(antecedent, consequent, None)
        #when merging whether the protein is covered or not should be meaningless

        return result

    def getCoverageMode(self):
        """ Returns whether the coverage is done only by the antecedent = 1, consecuent or both = 3 """
        antecedent = self.getCoverageFraction(self.MODE_ANTECEDENT) > 0
        consequent = self.getCoverageFraction(self.MODE_CONSEQUENT) > 0

        if antecedent and consequent:
            return self.MODE_BOTH
        elif antecedent:
            return self.MODE_ANTECEDENT
        elif consequent:
            return self.MODE_CONSEQUENT
        else:
            return None



class RuleCoverage(object):
    """ Performs the coverage operations for a set of rules against a set of proteins """

    ANTECEDENT = 1
    CONSEQUENT = 2
    BOTH = 3

    def __init__(self, pFile, rFile, cFile, exportType, onlyCovered = False):
        """ Create an instance by specifying the rule file, the coverage file to where dump the results,
        the export mode and the protein file that will be checked against the rules """
        self.coverageFile = cFile
        self.ruleFile = rFile
        self.proteinFile = pFile
        self.export = self.exportType(exportType)
        self.onlyCovered = onlyCovered

    def exportType(self, exportType):
        """ Defines the export types available """

        vector = RuleCoverageExportToVector(self.coverageFile)
        xyz = RuleCoverageExportToXYZ(self.coverageFile)
        image = RuleCoverageExportToImage(self.coverageFile)
        html = RuleCoverageExportToHtml(self.coverageFile)
        csv = RuleCoverageExportToCsv(self.coverageFile)

        exportTypes = {
            'vector': vector,
            'xyz': xyz,
            'image': image,
            'html': html,
            'csv': csv,
        }

        return exportTypes[str(exportType)]
        

    def updateOcurrenceVector(self, vector, ruleItem, ocurrences, modifier):
        """ Update the ocurrence vector based on the rule item and its ocurrences. Sets the modifier in the vector """
        ruleLength = len(ruleItem)
        for ocurr in ocurrences:
            for pos in range(0, ruleLength):
                if vector[pos+ocurr] != modifier:
                    vector[pos+ocurr] = vector[pos+ocurr] + modifier

        return vector

    
    def getCoverageOfRuleForProtein(self, protein, rule):
        """ Calculates the coverage vector for a protein and a particular rule """
        encoding = protein.getEncoding()
        antecedentVector = [0 for p in encoding]
        consequentVector = [0 for p in encoding]

        consequentOcurrences = [m.start() for m in re.finditer(rule.consequent, encoding)]
        consequentVector = self.updateOcurrenceVector(consequentVector, rule.consequent, consequentOcurrences, self.CONSEQUENT)
        isCovered = len(consequentOcurrences) > 0

        for antecedent in rule.antecedent:
            antecedentOcurrences = [m.start() for m in re.finditer(antecedent, encoding)]
            antecedentVector = self.updateOcurrenceVector(antecedentVector, antecedent, antecedentOcurrences, self.ANTECEDENT)
            isCovered = (len(antecedentOcurrences) > 0) and isCovered

        if self.onlyCovered and not(isCovered):
            antecedentVector = [0 for x in antecedentVector]
            consequentVector = [0 for x in consequentVector]

        coverageResult = RuleCoverageResult(antecedentVector, consequentVector, isCovered)
        return coverageResult

    def getCoverageOfRulesForProtein(self, protein, rules):
        """ Compute the coverage vector for a list of rules """
        result = None
        for r in rules:
            if result is None:
                result = self.getCoverageOfRuleForProtein(protein, r)

            else:
                result = result.mergeWith(self.getCoverageOfRuleForProtein(protein, r))

        return result

    def openRules(self):
        """ Open & parse the rules from the specified rule file """
        rules = []
        with open(self.ruleFile, 'r') as infile:
            for line in infile:
                rules.append(Rule(line))

        return rules

    def process(self):
        """ Read the rules and store them. Then read the protein index file and compute the coverage
        for the rules against the protein. Store the result in the selected output option """
        
        ruleFileExtraData = {'total':0, 'covered':0} #Set extra parametrs for showing summary of coverage
        rootFolder = os.path.dirname(os.path.realpath(self.proteinFile)) + os.path.sep
        
        #Read the rules from the rulefile.
        rules = self.openRules()

        index = 0
        fp = FastaParser()
        #Read each protein
        with open(self.proteinFile, 'r') as pfile:
            for line in pfile:
                fp.readFile(line.strip())
                for protein in fp.getProteins():
                    coverageResult = self.getCoverageOfRulesForProtein(protein, rules)
                    resultVector = coverageResult.getResultVector()
                    ruleFileExtraData['covered'] = ruleFileExtraData['covered'] + len([k for k in resultVector if k > 0])
                    ruleFileExtraData['total'] = ruleFileExtraData['total'] + len(resultVector)

                    extraData = {'proteinFraction':coverageResult.getCoverageFraction()}
                    self.export.addData(resultVector, index, protein.getEncoding(), self.clearPath(protein.getFilename()), extraData)
                    index += 1
                    print("Coverage for protein %s...\n", str(index))

        self.export.export(ruleFileExtraData)

    def clearPath(self, pathname):
        """ Leave only the filename from a given path. For displaying purposes only """
        head, tail = ntpath.split(pathname)
        return tail or ntpath.basename(head)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("proteinFile", help="The file that contains the proteins to be analized")
    parser.add_argument("ruleFile", help="The file with the rules to check for coverage against the proteins")
    parser.add_argument("coverageFile", help="The coverage file to where to output the coverage results")
    parser.add_argument("exportType", help="The way in which to export the results. Options are: vector, image, xyz, csv", 
        default='vector')
    parser.add_argument("--onlyCovered", help="To consider or not only covered rules", 
        default=False, type=bool)

    args = parser.parse_args()

    rc = RuleCoverage(args.proteinFile, args.ruleFile, args.coverageFile, args.exportType, args.onlyCovered)
    rc.process()
    print("DONE!")

if __name__ == "__main__":
    # execute only if run as a script
    main()