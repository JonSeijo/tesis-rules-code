# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import os
import re
#rom fastaread import Protein,FastaParser
from rule_stats import RuleStats
from rulegroup import RuleGroupParser,Rule,ClusterRule,ClusterRuleMatch,OcurrenceMatrix
from base_graph import SimpleGraph

class RuleStatsTest(unittest.TestCase):
    
    def testEnsureParsingRules(self):
        protein = "AACCBBAJNBIYGIUBCOAUENOFIAUHEFUBNAI"
        ruleString = "{AC,CB} => {FI}"
        rs = RuleStats()
        
        r = Rule(ruleString)
        self.assertEqual(r.consequent,  "FI")
        self.assertEqual(r.antecedent, ["AC", "CB"])

    def testNumberOfRepeats(self):
        protein = "AACCBBAJNBIYGIUBCOAUEACNOFIAUHECBFUBACNAI"
        ruleString = "{AC, CB} => {FI}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.numberOfRepeats("FI", protein), 1)
        self.assertEqual(rs.numberOfRepeats("CB", protein), 2)
        self.assertEqual(rs.numberOfRepeats("AC", protein), 3)

    def testDistanceOfSuccessiveRepeats(self):
        protein = "AACCBBAJNBIYGIUBCOAUEACNOFIAUHECBFUBACNAI"
        ruleString = "{AC, CB} => {FI}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("FI", protein), [])
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("CB", protein), [28])
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("AC", protein), [20,15])

    def testOcurrenceInRuleTypeOverlapped(self):
        protein = "AJOIMLKJCIUASLISHGAHFOAISNFAOSIFANCAOUSHOAISHCUANSOUHAOSODAOSI"
        ruleString = "{LISH, SHGA} => {ISHG}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.ocurrenceType(r, protein), RuleStats.OVERLAPPING)

    def testOcurrenceInRuleTypeIsolated(self):
        protein = "AACCBBAJNBIYGIUBCOAUEACNOFIAUHECBFUBACNAI"
        ruleString = "{AC, CB} => {FI}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.ocurrenceType(r, protein), RuleStats.ISOLATED)

    def testOcurrenceInRuleTypeMixed(self):
        protein = "AJOIMLKJCIUASHFOAILISHGASNFAOSIFANCAOUSHOAISHCUANSOUHAOSOISHGSI"
        ruleString = "{LISH, SHGA} => {ISHG}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.ocurrenceType(r, protein), RuleStats.MIXED)


    def testOcurrenceInRuleTypeOverlapped2(self):
        protein = "AAJAOIFJOAAABLKASIFJSAOFIJASOFMCNBOIJOAISJOFA"
        ruleString = "{AAAB, ABLK} => {ABL}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.ocurrenceType(r, protein), RuleStats.OVERLAPPING)

    def testOcurrenceInRuleTypeIsolated2(self):
        protein = "AAJAOIFJOAAABLKAOMMISIFJSAOMMIFIJASOFMCNBOIJOAISJOFAMMI"
        ruleString = "{AAAB, ABLK} => {MMI}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.ocurrenceType(r, protein), RuleStats.ISOLATED)

    def testOcurrenceInRuleTypeMixed2(self):
        protein = "AAJAOIFJOAAABLKASIFJSAOFIJASOFMCNBOIJOAISJOFABL"
        ruleString = "{AAAB, ABLK} => {ABL}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.ocurrenceType(r, protein), RuleStats.MIXED)

    def testOcurrenceIndexes(self):
        protein = "AACCBBAJNBIYGIUBCOAUEACNOFIAUHEFUBACNAI"
        ruleString = "{AC, CB} => {FI}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.getOcurrencesIndexes("CB", protein), [4])
        self.assertEqual(rs.getOcurrencesIndexes("AC", protein), [2,22,35])

    def testListOfOcurrencesRepeats(self):
        protein = "AACCBBAJNBIYGIUBCOAUEACNOFIAUHEFUBACNAI"
        ruleString = "{AC, CB} => {FI}"
        rs = RuleStats()
        r = Rule(ruleString)

        l = []
        for ant in r.antecedent:
            l.append(rs.getOcurrencesIndexes(ant, protein))

        self.assertEqual(l, [[2,22,35],[4]])

    def testAvgOfRepeats(self):
        protein = "AACCBBAJNBIYGIUBCOAUEACNOFIAUHEFUBACNAI"
        ruleString = "{AC, CB} => {FI}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.averageOcurrence(rs.distanceBetweenConsecutiveRepeats("CB", protein)), None)
        self.assertAlmostEqual(rs.averageOcurrence(rs.distanceBetweenConsecutiveRepeats("AC", protein)), 16.5)

    def testListOfAvgs(self):
        protein = "AACCBBAJNBIYGIUBCOAUEACNOFIAUHEFUBACNAI"
        ruleString = "{AC, CB} => {FI}"
        rs = RuleStats()
        r = Rule(ruleString)

        l = []
        for ant in r.antecedent:
            l.append(rs.averageOcurrence(rs.distanceBetweenConsecutiveRepeats(ant, protein)))

        self.assertEqual(l, [16.5, None])

    def testParseStringToList(self):
        rs = RuleStats()
        s1 = "[]"
        s2 = "[210, 701, 315, 34]"
        s3 = "[210]"
        e1 = []
        e2 = [210, 701, 315, 34]
        e3 = [210]
        r1 = rs.parseStrToList(s1)
        r2 = rs.parseStrToList(s2)
        r3 = rs.parseStrToList(s3)

        self.assertEqual(r1, e1)
        self.assertEqual(r2, e2)
        self.assertEqual(r3, e3)

    def testParseRepeatsToDict1(self):
        rs = RuleStats()
        expected = {"LHLA": [1,2,4,5]}
        rs.addDistanceRepeats("LHLA", 1, "[1,2,4,5]")
        self.assertEqual(rs.distancesBetweenConsecutiveRepeatsByItem, expected)

    def testParseRepeatsToDict2(self):
        rs = RuleStats()
        expected = {"LHLA": [1,2,4,5,10], "TPLH": [33, 34]}
        rs.addDistanceRepeats("LHLA", 1, "[1,2,4,5]")
        rs.addDistanceRepeats("LHLA", 1, "[10]")
        rs.addDistanceRepeats("TPLH", 1, "[33,34]")
        rs.addDistanceRepeats("CACA", 1, "[]")
        rs.addDistanceRepeats("PEDO", 1, "0")
        self.assertEqual(rs.distancesBetweenConsecutiveRepeatsByItem, expected)

    def testCheckThatAtLeastOneMatches(self):
        self.assertTrue("GAVN" in ["ADVN", "GAVN", "TPLH"])
        self.assertFalse("AAVN" in ["ADVN", "GAVN", "TPLH"])

    def testFindInGroup(self):
        groupedItems = {
            "AA": ["AA", "BB"],
            "CC": ["CC"],
            "DD": ["DD", "EE"],
        }
        
        p1 = "XXXXXXAAXXXXXXX"
        p2 = "XXXXXXXXCCXXXXX"
        p3 = "XXXXBBXXXXXXXXX"
        p5 = "XXXXXXDDXXXXXXX"
        p4 = "XXXXXXXXXXXEEXX"

        rs = RuleStats()
        self.assertTrue(rs.findInGroup("AA", p1, groupedItems))
        self.assertFalse(rs.findInGroup("AA", p2, groupedItems))
        self.assertTrue(rs.findInGroup("AA", p3, groupedItems))
        self.assertFalse(rs.findInGroup("CC", p3, groupedItems))
        self.assertTrue(rs.findInGroup("CC", p2, groupedItems))
        self.assertFalse(rs.findInGroup("DD", p2, groupedItems))
        self.assertFalse(rs.findInGroup("DD", p1, groupedItems))
        self.assertFalse(rs.findInGroup("DD", p1, groupedItems))
        self.assertFalse(rs.findInGroup("DD", p3, groupedItems))
        self.assertTrue(rs.findInGroup("DD", p4, groupedItems))
        self.assertTrue(rs.findInGroup("DD", p5, groupedItems))

    def testItemsGrouped(self):
        rs = RuleStats()
        items = ["TPLH", "SPLH", "ADIN", "ADPN", "TALH", "ELLL"]
        graph = rs.buildDistanceGraph(SimpleGraph("graph"), items, rs.DEFAULT_DISTANCE_THRESHOLD)
        groupedItems,replacements = rs.getItemsGroupedByEditDistance(items)
        
        for key,val in groupedItems.items():
            val.sort()

        self.assertEqual(groupedItems["SPLH"], ["SPLH", "TALH", "TPLH"])
        self.assertEqual(groupedItems["ADIN"], ["ADIN", "ADPN"])
        self.assertEqual(groupedItems["ELLL"], ["ELLL"])

    def testItemsGrouped2(self):
        items = ["A","B","C","D"]
        rs = RuleStats()
        graph = rs.buildDistanceGraph(SimpleGraph("graph"), items, rs.DEFAULT_DISTANCE_THRESHOLD)
        groupedItems,replacements = rs.getItemsGroupedByEditDistance(items)

        for key,val in groupedItems.items():
            val.sort()

        self.assertEqual(groupedItems["A"], items)

    def testDistanceOfSuccessiveRepeatsWithSynonyms(self):
        protein = "AACCBBAJNBIYGIUBCOAUEACNOFIAUHECBFUBACNAI"
        ruleString = "{AC, CB} => {FI}"
        rs = RuleStats()
        r = Rule(ruleString)
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("FI", protein, "FI"), [])
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("CB", protein, "CB"), [28])
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("AC", protein, "AC"), [20,15])
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("FI", protein, "FI|CB"), [22,6])
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("CB", protein, "CB|CO"), [13,15])
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("AC", protein, "AC|BA|NB"), [4,3,13,14,1])
        self.assertEqual(rs.distanceBetweenConsecutiveRepeats("AC", protein, "BA|AC|NB"), [4,3,13,14,1])

    def testSynonyms(self):
        rs = RuleStats()
        items = ["TPLH", "SPLH", "ADIN", "ADPN", "TALH", "ELLL"]
        graph = rs.buildDistanceGraph(SimpleGraph("graph"), items, rs.DEFAULT_DISTANCE_THRESHOLD)
        groupedItems,replacements = rs.getItemsGroupedByEditDistance(items)

        for key,val in groupedItems.items():
            val.sort()
        synonyms = rs.getSynonyms(groupedItems)

        self.assertEqual(synonyms["SPLH"], ["SPLH", "TALH", "TPLH"])
        self.assertEqual(synonyms["TALH"], ["SPLH", "TALH", "TPLH"])
        self.assertEqual(synonyms["TPLH"], ["SPLH", "TALH", "TPLH"])
        self.assertEqual(synonyms["ADIN"], ["ADIN", "ADPN"])
        self.assertEqual(synonyms["ADPN"], ["ADIN", "ADPN"])
        self.assertEqual(synonyms["ELLL"], ["ELLL"])

    def testClusterizedRulesPatterns(self):
        rs = RuleStats()
        items = ['AAA', 'AAB', 'CAB', 'HAV', 'HBV', 'HCV', 'LBV', 'JME', 'JMT', 'JLE', 'JLT']
        graph = rs.buildDistanceGraph(SimpleGraph("graph"), items, rs.DEFAULT_DISTANCE_THRESHOLD)
        groupedItems,replacements = rs.getItemsGroupedByEditDistance(items)
        synonyms = rs.getSynonyms(groupedItems)

        testCase = [
            ["{JLT,AAB} => {AAA}", ['JLT|JMT|JME|JLE', 'CAB|AAA|AAB'], 'CAB|AAA|AAB'],
            ["{AAA,AAB} => {CAB}", ['CAB|AAA|AAB', 'CAB|AAA|AAB'], 'CAB|AAA|AAB'],
            ["{JLE,CAB} => {HBV}", ['JLT|JMT|JME|JLE', 'CAB|AAA|AAB'], 'HBV|HCV|LBV|HAV'],
            ["{AAB,HBV} => {JME}", ['CAB|AAA|AAB', 'HBV|HCV|LBV|HAV'], 'JLT|JMT|JME|JLE'],
            ["{HCV,CAB} => {JLE}", ['HBV|HCV|LBV|HAV', 'CAB|AAA|AAB'], 'JLT|JMT|JME|JLE'],
            ["{LBV,JMT} => {HAV}", ['HBV|HCV|LBV|HAV', 'JLT|JMT|JME|JLE'], 'HBV|HCV|LBV|HAV'],
            ["{JME,CAB} => {LBV}", ['JLT|JMT|JME|JLE', 'CAB|AAA|AAB'], 'HBV|HCV|LBV|HAV'],
        ]

        for t in testCase:
            rule = Rule(t[0], 1)
            clusterRule = ClusterRule(rule, synonyms)
            expectedAntecedentPattern = t[1]
            computedAntecedentPattern = clusterRule.antecedentPattern
            expectedAntecedentPattern.sort()
            computedAntecedentPattern.sort()
            expectedAntecedentPattern = [''.join(sorted(x)) for x in expectedAntecedentPattern]
            computedAntecedentPattern = [''.join(sorted(x)) for x in computedAntecedentPattern]

            computedConsequentPattern = ''.join(sorted(clusterRule.consequentPattern))
            expectedConsequentPattern = ''.join(sorted(t[2]))

            self.assertEqual(expectedAntecedentPattern, computedAntecedentPattern)
            self.assertEqual(expectedConsequentPattern, computedConsequentPattern)


def main():
    unittest.main()

if __name__ == '__main__':
    main()