# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import os
from rulegroup import *

from sys import argv, exit


class RuleGroupTest(unittest.TestCase):
    
    def testCreatedOk(self):
        """ Check that the object is created with the correct parameters """
        rg = RuleGroupParser("in", "out")
        self.assertEqual("in", rg.input)
        self.assertEqual("out", rg.output)

    def testParseRuleIntoParts(self):
        """ Check that rule is parsed ok """
        rg = RuleGroupParser("rule1.txt", "out")
        rule = rg.parseRule("{ENGA,LENG} => {LLEN}")
        self.assertEqual(rule.antecedent, ["ENGA","LENG"])
        self.assertEqual(rule.consequent, "LLEN")

        rule = rg.parseRule("{GNTP,LHLA,PLHL,TPLH} => {NTPL}")
        self.assertEqual(rule.antecedent, ["GNTP","LHLA","PLHL","TPLH"])
        self.assertEqual(rule.consequent, "NTPL")

    def testParseRuleIntoPartsWithBlanks(self):
        """ Check that rule is parsed ok """
        rg = RuleGroupParser("rule1.txt", "out")
        rule = rg.parseRule("{ENGA, LENG} => {LLEN }")
        self.assertEqual(rule.antecedent, ["ENGA","LENG"])
        self.assertEqual(rule.consequent, "LLEN")

    def testConsequentIsOverlapped(self):
        """ The consequent is an overlapping of the antecedents, for example {LISH,SHGA} => {ISHG}.
        LISH        GHLE        GWTA
          SHGA        LEVV        TALH
        -------     -----      --------
         ISHG        HLEV        WTAL

         "{ISHG,SHGA} => {LISH}" This one does not overlap

        """
        self.assertTrue(Rule("{LISH,SHGA} => {ISHG}").isOverlapping()) 
        self.assertTrue(Rule("{GHLE,LEVV} => {HLEV}").isOverlapping()) 
        self.assertTrue(Rule("{GWTA,TALH} => {WTAL}").isOverlapping()) 
        self.assertTrue(Rule("{GWTA,TALH} => {TALH}").isOverlapping()) 
        self.assertTrue(Rule("{GWTA,TALH} => {GWTA}").isOverlapping()) 
        self.assertTrue(Rule("{GAN,NTN,NAME} => {ANTNAM}").isOverlapping()) 
        self.assertTrue(Rule("{HVAA,PLHV} => {LHVA}").isOverlapping()) 
        self.assertTrue(Rule("{AGAD,EAGA,LLEA} => {LEAG}").isOverlapping()) 
        self.assertFalse(Rule("{GWTA,TALH} => {GWTL}").isOverlapping()) 
        self.assertFalse(Rule("{ISHG,SHGA} => {LISH}").isOverlapping()) 


    def testCombineParts(self):
        """ Combine to fragments if possible by analyzing suffixes and prefixes. If that's not possible just plain concatenation """
        r = Rule("{LISH,SHGA} => {ISHG}")
        l = r.combineParts("LISH", "SHGA")
        self.assertEqual(["LISHGA"], l)

        l = r.combineParts("GAN", "NTN")
        self.assertEqual(["GANTN"], l)
        
        l = r.combineParts("NAME", "NTN")
        self.assertEqual([], l)

        l = r.combineParts("NTN", "NAME")
        self.assertEqual(["NTNAME"], l)

        l = r.combineParts("GWTA", "TALH")
        self.assertEqual(["GWTALH"], l)

        l = r.combineParts("GWAA", "WAAR")
        self.assertEqual(["GWAAR"], l)

        l = r.combineParts("IIII", "III")
        e = ["IIII", "IIIII", "IIIIII"]
        l.sort()
        e.sort()
        self.assertEqual(e, l)

    def testGenerateNewRuleFromCombination(self):
        """ Checks that a new rule can be formed upon a successful combination """
        r = Rule("{LISH,SHGA} => {ISHG}")
        cands = r.generateCandidatesFromCombination(["LISH","SHGA"])
        self.assertEqual(cands, [["LISHGA"]])

        cands = r.generateCandidatesFromCombination(["GAN", "NTN"])
        self.assertEqual([["GANTN"]], cands)

        cands = r.generateCandidatesFromCombination(["LISH","SHGA", "KJJ"])
        self.assertEqual(cands, [["LISHGA", "KJJ"]])

        cands = r.generateCandidatesFromCombination(["GAN", "NTN", "KJJ"])
        self.assertEqual([["GANTN", "KJJ"]], cands)

        cands = r.generateCandidatesFromCombination(["GAN", "NTN", "NAME"])
        self.assertEqual([["GANTN", "NAME"], ["GAN", "NTNAME"]], cands)

        cands = r.generateCandidatesFromCombination(["GANTN", "NAME"])
        self.assertEqual([["GANTNAME"]], cands)

        cands = r.generateCandidatesFromCombination(["GAN", "NTN", "NAME", "EMIL"])
        self.assertEqual([["GANTN", "NAME", "EMIL"], ["GAN", "NTNAME", "EMIL"], ["GAN", "NTN","NAMEMIL"]], cands)

    def testConsequentIsOverlapped(self):
        """ Check that sometimes information is added by the rules' consequent """
        self.assertFalse(Rule("{LISH,SHGA} => {ISHG}").addsInfo()) 
        self.assertFalse(Rule("{GHLE,LEVV} => {HLEV}").addsInfo()) 
        self.assertFalse(Rule("{GWTA,TALH} => {WTAL}").addsInfo()) 
        self.assertFalse(Rule("{GAN,NTN,NAME} => {ANTNAM}").addsInfo())
        self.assertEqual("L",Rule("{ENGA,LENG} => {LLEN}").addedInfo())
        self.assertEqual("L",Rule("{DAGA,LDAG} => {LLDA}").addedInfo())
        self.assertEqual("L",Rule("{AGAD,EAGA,LEAG} => {LLEA}").addedInfo())

    def testRuleTypes(self):
        self.assertEqual(2,Rule("{AGAD,EAGA,LEAG} => {LLEA}").getRuleType())
        self.assertEqual(2,Rule("{DAGA,LDAG} => {LLDA}").getRuleType())
        self.assertEqual(1,Rule("{LISH,SHGA} => {ISHG}").getRuleType())
        self.assertEqual(3,Rule("{ALHV,TPLH} => {LHVA}").getRuleType())
        self.assertEqual(2,Rule("{AGAD,LEAG} => {LLEA}").getRuleType())
        self.assertEqual(3,Rule("{LHLA,PLHI} => {LHIA}").getRuleType())

    def testPatternsForClusterizedRules(self):
        synonyms = {
            "SPLH": ["SPLH", "TALH", "TPLH"],
            "TALH": ["SPLH", "TALH", "TPLH"],
            "TPLH": ["SPLH", "TALH", "TPLH"],
            "ADIN": ["ADIN", "ADPN"],
            "ADPN": ["ADIN", "ADPN"],
            "ELLL": ["ELLL"],
        }

        cr1 = ClusterRule(Rule("{ELLL,TPLH} => {ADIN}"), synonyms)
        cr2 = ClusterRule(Rule("{ELLL,ADIN} => {SPLH}"), synonyms)

        self.assertEqual(cr1.consequentPattern, "ADIN|ADPN")
        self.assertEqual(cr1.antecedentPattern, ["ELLL","SPLH|TALH|TPLH"])
        self.assertEqual(cr2.consequentPattern, "SPLH|TALH|TPLH")
        self.assertEqual(cr2.antecedentPattern, ["ELLL","ADIN|ADPN"])

    def testMatchPatternAgainstProtein(self):
        synonyms = {
            "SPLH": ["SPLH", "TALH", "TPLH"],
            "TALH": ["SPLH", "TALH", "TPLH"],
            "TPLH": ["SPLH", "TALH", "TPLH"],
            "ADIN": ["ADIN", "ADPN"],
            "ADPN": ["ADIN", "ADPN"],
            "ELLL": ["ELLL"],
        }

        cr1 = ClusterRule(Rule("{ELLL,TPLH} => {ADIN}"), synonyms)
        p1 = "XXXXXXXELLLXXXSPLHXXXXXXXADPNXXXADPN"
        expected = ["ELLL", "SPLH", "ADPN"]
        expected.sort()
        r1 = cr1.match(p1)
        r1.matches.sort()
        self.assertTrue(r1.match)
        self.assertEqual(r1.matches, expected)

        p2 = "XXXXXXXELLLXXXSPLHXXXXXXXADFDXXXADFD"
        r2 = cr1.match(p2)
        self.assertFalse(r2.match)

        p3 = "XXXXXXXELLLXXXKKKKXXXXXXXADPNXXXADPN"
        r3 = cr1.match(p3)
        self.assertFalse(r3.match)

    def testMatchPatternAgainstProtein2(self):
        synonyms = {
            "AA": ["A1", "A2", "A3"],
            "BB": ["B1", "B2"],
            "CC": ["C1", "C2"],
        }

        cr1 = ClusterRule(Rule("{AA,BB} => {CC}"), synonyms)
        p1 = "XXXXXXA3XXXXB1XXXXXXXXXXXC2XXX"
        expected = ["A3", "B1", "C2"]
        expected.sort()
        r1 = cr1.match(p1)
        r1.matches.sort()
        self.assertTrue(r1.match)
        self.assertEqual(r1.matches, expected)

        p2 = "XXXXXXXXXXXXXXXXXXAAXXBBXXXXXXXXXXX"
        r2 = cr1.match(p2)
        self.assertFalse(r2.match)

        p3 = "A2A1XXXXXB2XXXXC1"
        expected = ["A1", "A2", "B2", "C1"]
        expected.sort()
        r3 = cr1.match(p3)
        r3.matches.sort()
        self.assertTrue(r3.match)
        self.assertEqual(r3.matches, expected)

    def testClusterRuleCooccurence(self):
        synonyms = {
            "A1": ["A1", "A2", "A3"],
            "B1": ["B1", "B2"],
            "C1": ["C1", "C2"],
        }
        cr1 = ClusterRule(Rule("{A1,B1} => {C1}"), synonyms)
        p1 = "XXXXXXA1XXXXXXB2XXXXXXXXXXXXXXXXC1X"
        p2 = "XXXXXXA1XXXXXXB1XXXXXXXXXXXXXXXXC1X"

        items = []
        for key,itemList in synonyms.items():
            for item in itemList:
                items.append(item)

        occ = OcurrenceMatrix(items)
        res = cr1.match(p1)
        occ.addItems(res.matches)
        res = cr1.match(p2)
        occ.addItems(res.matches)

        self.assertEqual(occ.ocurrences["A1"]["C1"], 2)
        self.assertEqual(occ.ocurrences["C1"]["A1"], 2)
        self.assertEqual(occ.ocurrences["C1"]["B2"], 1)
        self.assertEqual(occ.ocurrences["B1"]["C1"], 1)

        #print(occ.printMatrix())

    def testClusterRuleCooccurence2(self):
        synonyms = {
            "A1": ["A1", "A2", "A3"],
            "B1": ["B1", "B2"],
            "C1": ["C1", "C2"],
        }
        cr1 = ClusterRule(Rule("{A1,B1} => {C1}"), synonyms)
        p1 = "XXXXXXA1XXXXXXB2XXXA1XXXXXXXXXXXC1X"
        p2 = "XXXXXXA1XXXXXXB1XXXXXXXXXXXXXXXXC1X"

        items = []
        for key,itemList in synonyms.items():
            for item in itemList:
                items.append(item)

        occ = OcurrenceMatrix(items)
        res = cr1.match(p1)
        occ.addItems(res.matches)
        res = cr1.match(p2)
        occ.addItems(res.matches)

        self.assertEqual(occ.ocurrences["A1"]["C1"], 2)
        self.assertEqual(occ.ocurrences["C1"]["A1"], 2)


def main():
    unittest.main()

if __name__ == '__main__':
    main()