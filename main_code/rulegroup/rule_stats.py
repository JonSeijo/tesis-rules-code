# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import sys
import argparse
import re
import sys
import ast
import sqlite3

from main_code.rulegroup.fastaread import Protein
from main_code.rulegroup.rulegroup import Rule, ClusterRule,ClusterRuleMatch,OcurrenceMatrix
from main_code.rulegroup.base_graph import GraphvizGraph, SimpleGraph
from main_code.rulegroup.metrics import StringMetrics

# TODO: jonno: Refactorizar para que use el nuevo DBController
class RuleStats(object):
    """ Compute stats for a set of rules. Modify the DB adding the
    neccessary data. Computes distance between repetitions, average repitions for both
    consequents and antecedents. It does the same job but considering
    items alone and their function (cons or ant) in the whole set of rules. """

    #Ocurrence type constants
    ISOLATED = 1
    OVERLAPPING = 2
    MIXED = 3

    #Item function constants
    ANTECEDENT = 1
    CONSEQUENT = 2

    #Mode constants
    SYNONYMS_ONLY = 1
    CHECK_ANTECEDENTS = 2

    #Default distance threshold when computing Levenshtein on auxiliary functions
    DEFAULT_DISTANCE_THRESHOLD = 2

    def __init__(self, filename="protein-rules.db"):
        """ Build the object and connect to the DB """
        super(RuleStats, self).__init__()
        self.filename = filename

        # TODO: Por que estaba comentado esto?
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

        self.ocurrenceCache = {}
        self.distancesBetweenConsecutiveRepeatsByItem = {}

    # def __del__(self):
        # self.connection.close()


    def putInCache(self, key, value):
        """ Caches values in an dictionary in order to avoid recomputing things """
        if len(self.ocurrenceCache) > 20:
            self.ocurrenceCache = {}
        self.ocurrenceCache[key] = value


    def getOcurrencesIndexes(self, repeat, protein, customPattern = None):
        """ Return the indexes of the ocurrences of repeat inside a protein """
        repeatsPositions = []
        regex = repeat
        if customPattern is not None:
            regex = customPattern

        #Try finding in the cache
        key = regex + "-" + protein
        #if key in self.ocurrenceCache:
        #    return self.ocurrenceCache[key]

        pattern = re.compile("(?=("+regex+"))", re.IGNORECASE)
        for m in pattern.finditer(protein):
            repeatsPositions.append(m.start()+1) #+1 so they start in 1 not 0

        #self.putInCache(key, repeatsPositions)
        return repeatsPositions

    def numberOfRepeats(self, repeat, protein, customPattern = None):
        """ Return the number of repeats of a repeating subsequence in a protein """
        return len(self.getOcurrencesIndexes(repeat, protein, customPattern))

    def distanceBetweenConsecutiveRepeats(self, repeat, protein, customPattern = None):
        """ Compute the distance between consecutive repeating subsequences in a protein """
        res = []
        repeatsPositions = self.getOcurrencesIndexes(repeat, protein, customPattern)

        if len(repeatsPositions) > 1:
            for i in range(1, len(repeatsPositions)):
                res.append(repeatsPositions[i] - repeatsPositions[i-1])

        return res

    def ocurrenceType(self, rule, protein):
        """ Get the ocurrence type of a rule in a protein """
        overlaps = 0
        isolated = 0

        consequent = rule.consequent
        consequentPositions = self.getOcurrencesIndexes(rule.consequent, protein)
        overlappingOcurrences = dict()
        for x in consequentPositions:
            overlappingOcurrences[x] = False

        if len(consequentPositions) == 0:
            print("ERROR! There must be an ocurrence of a consequent!")
            sys.exit(-1)

        for cPos in consequentPositions:
            for antecedent in rule.antecedent:
                antecedentPositions = self.getOcurrencesIndexes(antecedent, protein)
                for start in antecedentPositions:
                    end = start + len(antecedent)
                    if cPos >= start and cPos <= end:
                        #Overlaps
                        overlaps = RuleStats.OVERLAPPING
                        overlappingOcurrences[cPos] = True

        if any(value == False for key, value in overlappingOcurrences.items()):
            isolated = RuleStats.ISOLATED

        return overlaps+isolated

    def averageOcurrence(self, listOfOcurrences):
        """ Returns the average ocurrence from the list of ocurrences """
        result = None
        if len(listOfOcurrences) > 0:
            result = sum(listOfOcurrences)/len(listOfOcurrences)
        return result

    def itemIterator(self):
        """ Returns a sqlite iterator to the distinct items"""
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        res = cursor.execute('''SELECT DISTINCT(item) FROM item''')
        # connection.close() # jonno: Originalmente descomentado en Enriquez
        return res

    def ruleIterator(self):
        """ Returns an iterator to the rule data table """
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        res = cursor.execute('''SELECT rule FROM rule''')
        # connection.close() # jonno: Originalmente descomentado en Enriquez
        return res


    def groupFrequencyDataByDistance(self, items):
        """ Group frequencies by distance """
        groupedItems = {}

        graph = self.buildDistanceGraph(SimpleGraph("graph"), list(items.keys()), self.DEFAULT_DISTANCE_THRESHOLD)
        rd = graph.buildReplacementMap()
        for item,count in items.items():
            replacementKey = rd[item]
            if replacementKey not in groupedItems.keys():
                groupedItems[replacementKey] = 0
            groupedItems[replacementKey] += count
        return groupedItems

    def getSynonyms(self, groupedItems):
        """ Returns a dictionary of item -> synonyms of that item. Keys are generated based on a candidate of each group """
        synonyms = {}
        for key,values in groupedItems.items():
            for val in values:
                synonyms[val] = values

        return synonyms

    def getItemsGroupedByEditDistance(self, items):
        """ Receives an item list and returns a dictionary of the item groups keyed by a candidate.
        Each group is formed by edit distance threshold values. Also returns a the replacement map (item -> candidate) """
        graph = self.buildDistanceGraph(SimpleGraph("graph"), items, self.DEFAULT_DISTANCE_THRESHOLD)
        replacements = graph.buildReplacementMap()
        groupedItems = {}
        for item in items:
            candidate = replacements[item] 
            if candidate not in groupedItems:
                groupedItems[candidate] = []
            groupedItems[candidate].append(item)

        return (groupedItems, replacements) 

    def findInGroup(self, item, proteinStr, groupedItems):
        """ Finds an item in a protein string but also checking the item's synonym """
        found = False
        pattern = re.compile('|'.join(groupedItems[item]), re.IGNORECASE)
        return pattern.search(proteinStr) is not None

    def getItemsFromCoverages(self):
        items = []
        #Fetch items from item table
        for itemRow in self.itemIterator():
            items.append(itemRow[0])
        return items

    def getItemsFromRules(self):
        #Iterate over rules and extract items
        items = set()
        for ruleRow in self.ruleIterator():
            rule = Rule(ruleRow[0]) #parse current rule
            
            items.add(rule.consequent)
            for antecedent in rule.antecedent:
                items.add(antecedent)
        return list(items)

    def writeFrecuencies(self, items, total, title, file):
        """ Write the item counts of the dictionary to the file with title and total """
        file.write(title + " - total: " + str(total) +"\n")
        for item in sorted(items.keys()):
            #freq = float(count) / float(total)
            freq = items[item]
            file.write(item + "\t" + str(freq) + "\n")
        file.write("\n")

    def computeFrequencies(self, groupedByEditDistance = False):
        """ Computes the frequencies of items in both proteins and rules """
        ocurrencesInProteins = {}
        ocurrencesInRules = {}
        qtyRules = 0
        qtyProteins = 0
        groupedItems = {}
        replacementMap = {}
        
        #items = self.getItemsFromCoverages() # jonno: Originalmente comentado en Enriquez
        items = self.getItemsFromRules()

        if groupedByEditDistance:
            groupedItems, replacementMap = self.getItemsGroupedByEditDistance(items)
            items = list(groupedItems.keys())

        for item in items:
            ocurrencesInRules[item] = 0
            ocurrencesInProteins[item] = 0
            
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        #Fetch rows and search for item repeats in rows
        for proteinRow in cursor.execute("SELECT encoding FROM protein"):
            qtyProteins = qtyProteins + 1
            for item,count in ocurrencesInProteins.items():
                actual = 0
                if groupedByEditDistance:
                    actual = self.findInGroup(item, proteinRow[0], groupedItems)
                else:
                    #actual = self.numberOfRepeats(item, proteinRow[0])
                    if self.numberOfRepeats(item, proteinRow[0]) > 0:
                        actual = 1
                ocurrencesInProteins[item] = count + actual

        #Iterate over rules and match them against items
        for ruleRow in self.ruleIterator():
            qtyRules = qtyRules + 1
            rule = Rule(ruleRow[0]) #parse current rule

            if groupedByEditDistance:
                matched = []
                candidate = replacementMap[rule.consequent]
                ocurrencesInRules[candidate] = ocurrencesInRules[candidate] + 1
                matched.append(candidate)

                for antecedent in rule.antecedent:
                    candidate = replacementMap[antecedent]
                    if candidate not in matched:
                        ocurrencesInRules[candidate] = ocurrencesInRules[candidate] + 1
                        matched.append(candidate)
            else:
                self.addOcurrence(ocurrencesInRules, rule.consequent)
                for antecedent in rule.antecedent:
                    self.addOcurrence(ocurrencesInRules, antecedent)
        
        pfile = open("protein.tsv", 'w')
        rfile = open("rule.tsv", 'w')

        self.writeFrecuencies(ocurrencesInProteins, qtyProteins, "Proteins", pfile)
        self.writeFrecuencies(ocurrencesInRules, qtyRules, "Rules", rfile)
        
        pfile.close()
        rfile.close()


    def addOcurrence(self, counter, item):
        """ Adds ocurrence to the dictionary counter  """
        if item not in counter:
            counter[item] = 0    
        counter[item] = counter[item] + 1 


    def addDistanceRepeats(self, item, type, repeats):
        """ Adds repetition info to the instance's dictionary of item -> distance in repeats """
        parsedList = self.parseStrToList(repeats)
        if isinstance(parsedList, list) and len(parsedList) > 0:
            if item in self.distancesBetweenConsecutiveRepeatsByItem:
                self.distancesBetweenConsecutiveRepeatsByItem[item] = self.distancesBetweenConsecutiveRepeatsByItem[item] + parsedList
            else:
                self.distancesBetweenConsecutiveRepeatsByItem[item] = parsedList


    def parseStrToList(self, listAsString):
        """ Parse the list formatted as a string into a real list """
        return ast.literal_eval(listAsString.strip())


    def writeDistancesToFile(self, file):
        """ Write distance data to file """
        file.write("item\tdistance\tconsequentType\n")
        for item,data in self.distancesBetweenConsecutiveRepeatsByItem.items():
            for distance in data:
                file.write(item + "\t" + str(distance) + "\n")


    def replaceConsequentOcurrenceTypeCode(self, code):
        """ Replace code with string for the ocurrence type of the consequent """
        codes = {self.ISOLATED:"Aislada", self.OVERLAPPING:"Solapada", self.MIXED:"Mixta"}
        return codes[code]

    def getDistancesForItems(self, groupedByEditDistance = False, mode = None):
        """ Computes the distances for consecutive repeats of items in the proteins. According to the grouping option and mode different criterias are used """
        if mode is None:
            mode = self.SYNONYMS_ONLY

        connection = sqlite3.connect(self.filename)
        otherCursor = connection.cursor()

        coverageIterator = otherCursor.execute('''
            SELECT r.consequent, rc.consequentRepeatsDistances, rc.consequentOcurrenceType, rc.idProtein, p.encoding, r.rule, r.idRule FROM rule_coverage rc 
                INNER JOIN rule r ON rc.idRule = r.idRule
                INNER JOIN protein p on rc.idProtein = p.idProtein
                -- WHERE rc.idProtein IN (38077,27)
                GROUP BY rc.idProtein, r.consequent
                -- LIMIT 10000
            ''')

        if groupedByEditDistance:
            self.computeDistancesWithGroups(self.itemIterator(), coverageIterator, groupedByEditDistance, mode)
        else:
            self.computeDistances(self.itemIterator(), coverageIterator)

        connection.commit()
        connection.close()

    def computeDistances(self, itemIterator, coverage):
        """ Generate the distance between consecutive repetitions for further analysis """
        items = []
        groupedItems = {}
        replacementMap = {}

        for row in itemIterator:
            items.append(row[0])

        file = open("distances.txt", 'w')   
        file.write("Item\tDistancia\tTipo\tidProtein\tidRule\tModo\n")
        
        for row in coverage:
            itemName = row[0]
            ocurrenceType = self.replaceConsequentOcurrenceTypeCode(row[2])
            distanceList = self.parseStrToList(row[1])
            if isinstance(distanceList, list) and len(distanceList) > 0:            
                for distance in distanceList:
                    file.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (itemName, distance, ocurrenceType, row[3], row[6], "NO-AGRUPADO"))
            
        file.close()

    def computeDistancesWithGroups(self, itemIterator, coverage, rules, mode = None):
        """ Generate the distance between consecutive repetitions for further analysis """
        if mode is None:
            mode = self.SYNONYMS_ONLY
        print("Grouping by edit distance graph with Levenshtein distance %d" % self.DEFAULT_DISTANCE_THRESHOLD)
        items = []
        groupedItems = {}
        replacementMap = {}

        for row in itemIterator:
            items.append(row[0])

        groupedItems, replacementMap = self.getItemsGroupedByEditDistance(items)
        synonyms = self.getSynonyms(groupedItems)

        file = open("distances.txt", 'w')   
        file.write("Item\tDistancia\tTipo\tidProtein\tidRule\tModo\n")

        # Add the rules keyed by consequent (eg rules = {"LISH": {{id1, id2, ...}}}
        rules = {}
        
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        otherCursor = connection.cursor()

        for r in otherCursor.execute('''SELECT idRule,consequent FROM rule'''):
            consequent = r[1].strip()
            if consequent not in rules:
                rules[consequent] = set()
            rules[consequent].add(r[0])
        
        for row in coverage:
            c = connection.cursor()
            idRulesThatCoverTheSameProtein = set()
            for r in c.execute('''SELECT idRule FROM rule_coverage WHERE idProtein = ?''', (row[3],)):
                idRulesThatCoverTheSameProtein.add(r[0]) 

            itemName = row[0]
            ocurrenceType = self.replaceConsequentOcurrenceTypeCode(row[2])
            graphMode = ""
            if mode == self.SYNONYMS_ONLY:
                pattern = '|'.join(synonyms[itemName])
                graphMode = "MODO-1"
            else:
                graphMode = "MODO-2"
                toCheck = [itemName]
                for syn in synonyms[itemName]:
                    #For each synonyms, check in which rules is present and if they apply to the current protein as well.
                    if syn in rules and len(rules[syn].intersection(idRulesThatCoverTheSameProtein)) > 0 and syn not in toCheck:
                        toCheck.append(syn)
                pattern = '|'.join(toCheck)

            distanceList = self.distanceBetweenConsecutiveRepeats(itemName, row[4], pattern)

            #ocurrenceType = self.replaceConsequentOcurrenceTypeCode(self.ocurrenceType(Rule(row[5]), row[4])) #match the new ocurrence
            candidate = synonyms[itemName][0]
            if isinstance(distanceList, list) and len(distanceList) > 0:            
                for distance in distanceList:
                    file.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (candidate, distance, ocurrenceType, row[3], row[6], graphMode))
            
        file.close()
        connection.commit()
        connection.close()

    def rulesAndItemsForClusteringetItemsGroupedByEditDistance(self, ruleIterator):
        """ Get rules and items for cluster analysis """
        rules = []
        items = []
        for row in ruleIterator:
            rule = Rule(row[1], row[0])
            rules.append(rule)
            for a in rule.antecedent:
                items.append(a)
            items.append(rule.consequent)

        items = list(set(items))
        return (rules,items)
        

    def computeDistancesWithClusterizedRules(self, outputFilename="ocurrence_matrix.txt", outputClusterFilename="distances_cluster.txt"):
        """ Compute distances with clusterized rules. In the same pass compute the ocurrence matrix for the items for each protein"""
        groupedItems = {}
        replacementMap = {}

        connection = sqlite3.connect(self.filename)
        c = connection.cursor()

        rules, items = self.rulesAndItemsForClusteringetItemsGroupedByEditDistance(c.execute("SELECT idRule, rule FROM rule"))
        groupedItems, replacementMap = self.getItemsGroupedByEditDistance(items)
        synonyms = self.getSynonyms(groupedItems)
        clusterizedRules = self.getClusterizedRules(rules, synonyms)
        ocurrenceMatrix = OcurrenceMatrix(items)

        file = open(outputClusterFilename, "w")   
        file.write("Item\tDistancia\tTipo\tidProtein\tidRule\tModo\n")

        #i = 0
        for row in c.execute("SELECT encoding FROM protein"): #For each protein
            #i = i+1
            #if i%1000 == 0:
            #    print("Protein #"+str(i))
            
            proteinEncoding = row[0]
            toWrite = []
            for cr in clusterizedRules: #For each rule
                result = cr.match(proteinEncoding)
                if result.match:
                    distanceList = self.distanceBetweenConsecutiveRepeats(cr.rule.consequent, proteinEncoding, cr.consequentPattern)
                    candidate = synonyms[cr.rule.consequent][0]
                    for distance in distanceList:
                        toWrite.append("%s\t%s\t%s\t%s\t%s\t%s\n" % (candidate, distance, 'N/A', 'N/A', cr.rule.idRule, "CLUSTER"))

                    ocurrenceMatrix.addItems(result.matches)

            #Write data to file
            for tw in toWrite:
                file.write(tw)

        file.close()
        # Now Output the occurrence matrix
        file = open(outputFilename, "w")
        file.write(ocurrenceMatrix.printMatrix())
        file.close()

        connection.commit()
        connection.close()


    def getClusterizedRules(self, rules, synonyms):
        """ Returns a list of clusterized rules according to the synonyms received """
        clusterizedRules = []
        for rule in rules:
            clusterizedRules.append(ClusterRule(rule, synonyms))
        return clusterizedRules

    def buildDistanceGraph(self, graph, items, threshold):
        """ Builds the distance graph using levenshtein distance """
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                editDistance = StringMetrics.levenshtein(items[i], items[j])
                if editDistance < threshold:
                    graph.addLink(items[i], items[j])
                else:
                    graph.addNode(items[i])
                    graph.addNode(items[j])

        return graph

    def makeEditDistanceGraph(self, threshold):
        """ Calculates the Levenshtein distance for items and graph them according to the threshold """
        graph = GraphvizGraph("edit-distance.dot", "edit-distance.png", "graph", "Distancia de edición (Levenshtein(s1,s2) < " + str(threshold) + ")")
        items = set()
        for ruleRow in self.ruleIterator():
            rule = Rule(ruleRow[0])

            items.add(rule.consequent)
            for ant in rule.antecedent:
                items.add(ant)

        items = list(items)
        graph = self.buildDistanceGraph(graph, items, threshold)
        graph.graph()                

    def getControlDistances(self, outputFilename="distances_control.txt"):
        """ Takes every item and every rule and generates the distances_file according to whether they match and 
        at which distance no matter the coverage. """
        file = open(outputFilename, "w")   
        file.write("Item\tDistancia\tTipo\tidProtein\tidRule\tModo\n")

        items = set()
        for row in self.itemIterator():
            #if len(items) < 50:
            items.add(row[0])
        print("Leídos %d ítems..." % len(items))

        i = 0
        connection = sqlite3.connect(self.filename)
        c = connection.cursor()
        for row in c.execute("SELECT encoding,idProtein FROM protein"): #For each protein
            i = i+1
            if i%1000 == 0:
                print("Protein #"+str(i))
            
            proteinEncoding = row[0]
            toWrite = []
            for item in items: #For each items
                distanceList = self.distanceBetweenConsecutiveRepeats(item, proteinEncoding)
                for distance in distanceList:
                    toWrite.append("%s\t%s\t%s\t%s\t%s\t%s\n" % (item, distance, 'N/A', row[1], 'N/A', "CONTROL"))

            #Write data to file
            for tw in toWrite:
                file.write(tw)

        file.close()
        connection.commit()
        connection.close()

    def getNotCoveredProteinsDistances(self, outputFilename="distances_not_covered.txt"):
        """ Takes every item and every rule and generates the distances_file according to whether they match and 
        at which distance no matter the coverage. """
        file = open(outputFilename, "w")   
        file.write("Item\tDistancia\tTipo\tidProtein\tidRule\tModo\n")

        items = set()
        for row in self.itemIterator():
            #if len(items) < 50:
            items.add(row[0])
        print("Leídos %d ítems..." % len(items))

        i = 0
        c = self.connection.cursor()
        for row in c.execute("SELECT encoding,idProtein FROM protein WHERE idProtein NOT IN (SELECT DISTINCT(idProtein) from rule_coverage)"): #For each protein
            i = i+1
            if i%1000 == 0:
                print("Protein #"+str(i))
            
            proteinEncoding = row[0]
            toWrite = []
            for item in items: #For each items
                distanceList = self.distanceBetweenConsecutiveRepeats(item, proteinEncoding)
                for distance in distanceList:
                    toWrite.append("%s\t%s\t%s\t%s\t%s\t%s\n" % (item, distance, 'N/A', row[1], 'N/A', "NO-CUBIERTAS"))

            #Write data to file
            for tw in toWrite:
                file.write(tw)

        file.close()

    def getComplementControlDistances(self, outputFilename="distances_complement_control.txt"):
        """ Takes every item and every rule and generates the distances_file according to whether they match and 
        at which distance no matter the coverage. """
        file = open(outputFilename, "w")   
        file.write("Item\tDistancia\tTipo\tidProtein\tidRule\tModo\n")

        items = set()
        for row in self.itemIterator():
            items.add(row[0])
        print("Leídos %d ítems..." % len(items))

        i = 0
        for item in items:
            i = 0
            toWrite = []
            c = self.connection.cursor()
            for row in c.execute('''SELECT encoding,idProtein FROM protein WHERE idProtein NOT IN 
                (SELECT idProtein FROM rule_coverage WHERE idRule IN (SELECT idRule FROM rule WHERE consequent LIKE ?))''', [item]): #For each protein
                
                proteinEncoding = row[0]
                distanceList = self.distanceBetweenConsecutiveRepeats(item, proteinEncoding)
                for distance in distanceList:
                    toWrite.append("%s\t%s\t%s\t%s\t%s\t%s\n" % (item, distance, 'N/A', row[1], 'N/A', "CONTROL-COMPLEMENT"))

            #Write data to file
            for tw in toWrite:
                file.write(tw)

        file.close()


def parameterNotSet(param):
    """ Returns whether the parameter param is set """
    return param is None or len(param) == 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help="Filename for the SQLite database", type=str, default="protein-rules.db")
    parser.add_argument('--mode', help="Operation mode", type=str)
    parser.add_argument('--edt', help="Edit distance threshold", type=int, default=1)
    parser.add_argument('--ged', help="Group by Edit Distance Graph", type=int, default=0)
    parser.add_argument('--groupingmode', help="Grouping mode for synonyms of items", type=int, default=RuleStats.SYNONYMS_ONLY)

    args = parser.parse_args()

    ged = False
    if args.ged == 1:
        ged = True

    if parameterNotSet(args.filename):
        print("ERROR: filename for the database required and not set!! - Exiting...")
        sys.exit(-1)

    if parameterNotSet(args.mode):
        print("ERROR: mode is a required parameter and it is not set!! - Exiting...")
        sys.exit(-1)

    rs = RuleStats(args.filename)

    if args.mode == "freq":
        print("Calculating frequencies stats...")
        rs.computeFrequencies(ged)
    elif args.mode == "distances":
        print("Calculating distances stats...")
        rs.getDistancesForItems(ged, args.groupingmode)
    elif args.mode == "graph-distances":
        print("Calculating item distances and make a graph (edit distance)")
        rs.makeEditDistanceGraph(args.edt)
    elif args.mode == "cluster-distances":
        print("Calculating item distances with clusterized rules")
        rs.computeDistancesWithClusterizedRules()
    elif args.mode == "control-distances":  
        print("Calculating control distances...")
        rs.getControlDistances()
    elif args.mode == "complement-control-distances":  
        print("Calculating complement control distances...")
        rs.getComplementControlDistances()
    elif args.mode == "not-covered-distances":  
        print("Calculating distances for not covered proteins...")
        rs.getNotCoveredProteinsDistances()
    else:
        print("Invalid mode! Exiting")
        sys.exit(-1)

if __name__ == "__main__":
    # execute only if run as a script
    main()