# -*- coding: utf-8 -*-
#!/usr/bin/python

import itertools
import os
import argparse
import re
from pathlib import Path


class RuleGroupParser(object):
    """ Reads a file and process the rules in it according to the Rule's classification algorithms """

    def __init__(self, filename_input, filename_output):
        """ Creates an instance of the class for reading and writing the corresponding files """
        self.input = filename_input
        self.output = filename_output

    # TODO: Create parser that can handle rule_generator csv output directly
    def process(self):
        """ 
        Needs preprocessing, doesn't use rule_generator csv output.
        Open and process the file line by line in order to classify the rules acording to the Rule's own criteria 
        """
        separator = ";"
        outfile = open(self.output, 'w')

        with open(self.input) as infile:
            for line in infile:
                rule = self.parseRule(line)

                if rule.addsInfo():
                    group = "Agrega +"+rule.addedInfo()
                elif rule.isOverlapping():
                    group = "Overlapping"
                else:
                    group = "N/A"

                outline = rule.ruleRaw + separator + group + '\n'
                outfile.write(outline)

        outfile.close()

    def parseRule(self, ruleString):
        return Rule(ruleString)


class Rule(object):
    """ A rule is composed of a list of precedents and a consequent. Performs classification of rules according to the rule 
    morphology """

    OVERLAPPING = 1
    ADDS_INFO = 2
    OTHER = 3

    def __init__(self, ruleString, ruleId = None):
        """ Create a new Rule from a string """
        ruleString = ruleString.strip()
        if ruleId is not None:
            self.idRule = ruleId

        self.ruleRaw = ruleString
        s = ruleString.replace("{","").replace("}","").replace(" => ", ",")
        l = s.split(",")
        lastIndex = len(l)-1
        self.consequent = l[lastIndex].strip()
        self.antecedent = [x.strip() for x in l[0:lastIndex]]

    def addedInfo(self):
        """ Info added by the consequents in relation to the antecedents """
        added = []
        antecedents = ''.join(self.antecedent)
        for amino in self.consequent:
            if amino in antecedents:
                antecedents = antecedents.replace(amino, "", 1)
            else:
                added.append(amino)

        return ''.join(added)

    def addsInfo(self):
        """ whether a rule adds info or not """
        return len(self.addedInfo()) > 0


    def isOverlapping(self):
        """ Determine whether a rule's consequent is an overlapping of the antecedents """
        candidates = []
        for perm in itertools.permutations(self.antecedent):
            candidates.append(list(perm))           
            while len(candidates) > 0:
                current = candidates.pop()
                if self.consequent in "".join(current):
                    return True
                candidates = candidates + self.generateCandidatesFromCombination(current)

        return False

    def combineParts(self, part, otherPart):
        """ Combine to string if they have in common suffixes and prefixes """
        r = []
        
        #Check for part suffixes against otherPart prefixes
        for i in range(0, len(part)):
            suf = part[i:]
            if(otherPart.startswith(suf)):
                r.append(part[:i]+otherPart)

        return r

    def generateCandidatesFromCombination(self, listOfItems):
        """ Upon receiving a list of items, try to combine them and generate a new list with those combinations """
        r = []
        for i in range(0, len(listOfItems)-1):
            before = listOfItems[:i]
            after = listOfItems[i+2:]

            combination = self.combineParts(listOfItems[i], listOfItems[i+1])
            if len(combination) > 0:
                for c in combination:
                    r.append(before+[c]+after)

        return r

    def getRuleType(self):
        """ Get rule type according to the classification proposed """
        if self.isOverlapping():
            return self.OVERLAPPING
        elif self.addsInfo():
            return self.ADDS_INFO
        else:
            return self.OTHER

    def getRuleTypeText(self):
        """ Get rule text according to the classification proposed """
        if self.addsInfo():  # TODO: Redundante, calcula el added info dos veces
            return "Agrega +"+self.addedInfo()
        elif self.isOverlapping():
            return "Overlapping"
        else:
            return "N/A"

class ClusterRule(object):
    """ Models a clusterized version of the rule in which each part is searcheable
    through its synonyms """

    def __init__(self, rule, synonyms):
        self.rule = rule
        self.antecedentPattern = []
        self.antecedentSearchPattern = []
        self.consequentPattern = ""
        self.consequentSearchPattern = ""
        self.createPatterns(rule, synonyms)

    def createPatterns(self, rule, synonyms):
        """ Creates patterns for matching the clusterized rule to a protein """
        pat = "|".join(synonyms[rule.consequent])
        self.consequentPattern = pat
        self.consequentSearchPattern = re.compile("(?=("+pat+"))", re.IGNORECASE)

        for ant in rule.antecedent:
            pat = "|".join(synonyms[ant])
            self.antecedentPattern.append(pat)
            self.antecedentSearchPattern.append(re.compile("(?=("+pat+"))", re.IGNORECASE))

    def match(self, protein):
        """ Matches a protein with the clusterized version of the rule. Returns a ClusterRuleMatch object
        with the matching data and the result """
        
        match = ClusterRuleMatch(False, [])
        isMatch = False
        matches = re.findall(self.consequentSearchPattern, protein)
        isMatch = len(matches) > 0
        
        #If consequent didn't match return false
        if not isMatch:
            return match
        match.addMatches(matches)

        for pattern in self.antecedentSearchPattern:
            matches = re.findall(pattern, protein)
            isMatch = len(matches) > 0
            if not isMatch:
                return match
            match.addMatches(matches)

        if len(match.matches) > 0:
            match.match = True
        return match


class ClusterRuleMatch(object):

    def __init__(self, isMatch, matches):
        self.match = isMatch
        self.matches = matches

    def addMatches(self, listOfMatches):
        """ Add matches to the list of current matches """
        for m in list(set(listOfMatches)):
            if m not in self.matches:
                self.matches.append(m)


class OcurrenceMatrix(object):

    def __init__(self, items = None):
        """ Initialize the matrix based on the items received """
        self.ocurrences = {} #TODO: Improve storage!!
        if items != None:
            for i in items:
                self.ocurrences[i] = {}
                for j in items:
                    self.ocurrences[i][j] = 0

    def addItems(self, itemsToAdd):
        """ Add items to the occurrence matrix """
        for i in itemsToAdd:
            for j in itemsToAdd:
                if i != j:
                    self.ocurrences[i][j] = self.ocurrences[i][j] + 1
        #if "HBV" in itemsToAdd:
        #    print(self.ocurrences["HBV"])
        #    print("---------------------")

    def printMatrix(self):
        """ Return a textual representation of a string of the occurrence matrix """
        sep = "\t"
        output = sep
        for label in self.ocurrences.keys():
            output += label+sep
        output += "\n"


        for key,row in self.ocurrences.items():
            output += key+sep
            for kk,value in row.items():
                output += str(value)+sep

            output += "\n"
        return output



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="The input filename to where to extract the rules")
    parser.add_argument("outputFile", help="The output folder to place the sampled files")
    args = parser.parse_args()

    rg = RuleGroupParser(args.inputFile, args.outputFile)
    rg.process()


if __name__ == "__main__":
    # execute only if run as a script
    main()