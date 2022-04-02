# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import os
import re
from rulegroup import *
from rulecoverage import *

from sys import argv, exit


class RuleCoverageTest(unittest.TestCase):
    
    def testCoverageOfRulesReturnsAListOfTheSizeOfProtein(self):
        """ Check that the coverage returns a vector of the size of the protein """
        rule = Rule("{ERGA,LERG} => {LLER}")
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p','r','c', 'vector')
        self.assertEqual(len(p.getEncoding()), len(cov.getCoverageOfRuleForProtein(p,rule).getResultVector()))

    def testOcurrencesAreFoundInProtein(self):
        """ Subparts of string are correctly found """
        self.assertEqual([0], [m.start() for m in re.finditer("ERGA", "ERGALERGLLER")])
        self.assertEqual([4], [m.start() for m in re.finditer("LERG", "ERGALERGLLER")])
        self.assertEqual([8], [m.start() for m in re.finditer("LLER", "ERGALERGLLER")])

    def testCoverageOfRulesReturnsTheOccurrencesOfRuleInTheProtein(self):
        """ Check that the coverage returns a vector of the size of the protein """
        rule = Rule("{ERGA,LERG} => {LLER}")
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p','r','c', 'vector')
        ocurrences = [1,1,1,1,1,1,1,1,2,2,2,2]
        self.assertEqual(ocurrences, cov.getCoverageOfRuleForProtein(p,rule).getResultVector())

    def testCoverageOfRulesReturnsTheOccurrencesOfRuleInTheProtein2(self):
        """ Check that the coverage returns a vector of the size of the protein """
        rule = Rule("{GADV,GHLE} => {TPLH}")
        enc = "SDLGKKLLEAARAGQDDEVRILMANGADVNANDWFGITPLHLVVNNGHLEIIEVLLKYAADVNASDKSGWTPLHLAAYRGHLEIVEVLLKYGADVNAMDYQGYTPLHLAAEDGHLEIVEVLLKYGADVNAQDKFGKTAFDISIDNGNEDLAEILQ"
        p = Protein(enc, ">dummy")
        cov = RuleCoverage('p','r','c', 'vector')
        ocurrences = [0 for c in range(0, len(enc))]

        for ant in ["GADV","GHLE"]:
            for ocur in [m.start() for m in re.finditer(ant, enc)]:
                for index in range(0, len(ant)):
                    ocurrences[ocur+index] = 1

        for ocur in [m.start() for m in re.finditer("TPLH", enc)]:
                for index in range(0, len(ant)):
                    ocurrences[ocur+index] = 2

        self.assertEqual(ocurrences, cov.getCoverageOfRuleForProtein(p,rule).getResultVector())

    def testCoverageFractionForEachPart(self):
        """ Check that the coverage returns a vector of the size of the protein """
        rule = Rule("{ERGA,LERG} => {LLER}")
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p','r','c', 'vector')
        ocurrences = [1,1,1,1,1,1,1,1,2,2,2,2]
        coverageResult = cov.getCoverageOfRuleForProtein(p, rule)
        self.assertAlmostEqual(2.0/3.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_ANTECEDENT))
        self.assertAlmostEqual(1.0/3.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_CONSEQUENT))
        self.assertAlmostEqual(1.0, coverageResult.getCoverageFraction())

    def testCoverageDependingOnOnlyCovers(self):
        """ Check that the coverage returns different values if the coverage only considers rules that covers the proein """
        rule = Rule("{ERGA,LERG} => {PPPP}")
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p','r','c', 'vector')
        coverageResult = cov.getCoverageOfRuleForProtein(p, rule)
        self.assertAlmostEqual(2.0/3.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_ANTECEDENT))
        self.assertAlmostEqual(0.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_CONSEQUENT))
        self.assertAlmostEqual(2.0/3.0, coverageResult.getCoverageFraction())


    def testCoverageDependingOnOnlyCovers2(self):
        """ Check that the coverage returns different values if the coverage only considers rules that covers the proein """
        rule = Rule("{ERGA,LERG} => {PPPP}")
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p','r','c', 'vector', True)
        coverageResult = cov.getCoverageOfRuleForProtein(p, rule)
        self.assertAlmostEqual(0.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_ANTECEDENT))
        self.assertAlmostEqual(0.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_CONSEQUENT))
        self.assertAlmostEqual(0.0, coverageResult.getCoverageFraction())


    def testCoverageFractionForConsequent(self):
        """ Check that the coverage fraction of a consequent in a real rule is ok """
        rule = Rule("{GADV,GHLE} => {ADVNAND}")
        enc = "SDLGKKLLEAARAGQDDEVRILMANGADVNANDWFGITPLHLVVNNGHLEIIEVLLKYAADVNASDKSGWTPLHLAAYRGHLEIVEVLLKYGADVNAMDYQGYTPLHLAAEDGHLEIVEVLLKYGADVNAQDKFGKTAFDISIDNGNEDLAEILQ"
        p = Protein(enc, ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        self.assertAlmostEqual(7.0/len(enc), cov.getCoverageOfRuleForProtein(p,rule).getCoverageFraction(RuleCoverageResult.MODE_CONSEQUENT))

    def testCoverageComputedFromVariousRules(self):
        rules = [Rule("{ERGA,XXXX} => {XXXX}"), Rule("{XXXX,LERG} => {LLER}")]
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        self.assertAlmostEqual(2.0/3.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_ANTECEDENT))
        self.assertAlmostEqual(1.0, coverageResult.getCoverageFraction())

    def testCoverageComputedMode1(self):
        rules = [Rule("{ERGA,XXXX} => {XXXX}")]
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        self.assertEqual(1, coverageResult.getCoverageMode())

    def testCoverageComputedMode2(self):
        rules = [Rule("{XXX,XXXX} => {XXXX}")]
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        self.assertEqual(None, coverageResult.getCoverageMode())

    def testCoverageComputedMode3(self):
        rules = [Rule("{XXX,XXXX} => {LLER}")]
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        self.assertEqual(2, coverageResult.getCoverageMode())

    def testCoverageComputedMode4(self):
        rules = [Rule("{XXX,ERGA} => {LLER}")]
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        self.assertEqual(3, coverageResult.getCoverageMode())

    def testCoverageComputedFromVariousRulesDoesNotChangeIfRulesAreEqual(self):
        rules = [Rule("{ERGA,LERG} => {LLER}"), Rule("{ERGA,LERG} => {LLER}")]
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        self.assertAlmostEqual(2.0/3.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_ANTECEDENT))
        self.assertAlmostEqual(1.0, coverageResult.getCoverageFraction())

    def testCoverageComputedFromVariousRules2(self):
        rules = [Rule("{ERGA,LERG} => {XXXX}"), Rule("{ERGA,LERG} => {LLEM}")]
        p = Protein("ERGALERGLLER", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        coverageVector = [1,1,1,1,1,1,1,1,0,0,0,0]
        self.assertAlmostEqual(2.0/3.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_ANTECEDENT))
        self.assertAlmostEqual(0.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_CONSEQUENT))
        self.assertAlmostEqual(2.0/3.0, coverageResult.getCoverageFraction())
        self.assertEqual(coverageVector, coverageResult.getResultVector())

    def testCoverageComputedFromVariousRules3(self):
        rules = [Rule("{ERGA,LERG} => {XXXX}"), Rule("{ERGA,LERG} => {LLEM}")]
        p = Protein("ERGALERGLLERZZZZ", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        coverageVector = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
        self.assertAlmostEqual(0.5, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_ANTECEDENT))
        self.assertAlmostEqual(0.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_CONSEQUENT))
        self.assertAlmostEqual(0.5, coverageResult.getCoverageFraction())
        self.assertEqual(coverageVector, coverageResult.getResultVector())

    def testCoverageComputedFromVariousRules4(self):
        rules = [Rule("{ERGA,LERG} => {XXXX}"), Rule("{ERGA,ZZZZ} => {LERG}")]
        p = Protein("ERGALERGMMMMXXXX", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        coverageVector = [1,1,1,1,3,3,3,3,0,0,0,0,2,2,2,2]
        self.assertAlmostEqual(0.5, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_ANTECEDENT))
        self.assertAlmostEqual(0.5, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_CONSEQUENT))
        self.assertAlmostEqual(3.0/4.0, coverageResult.getCoverageFraction())
        self.assertEqual(coverageVector, coverageResult.getResultVector())

    def testCoverageComputedOnlyForOneAntecedent(self):
        rules = [Rule("{ERGA,LERG} => {XXXX}")]
        p = Protein("ZZZZERGAZZZZZZ", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        coverageResult = cov.getCoverageOfRulesForProtein(p,rules)
        coverageVector = [0,0,0,0,1,1,1,1,0,0,0,0,0,0]
        self.assertAlmostEqual(4.0/14.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_ANTECEDENT))
        self.assertAlmostEqual(0.0, coverageResult.getCoverageFraction(RuleCoverageResult.MODE_CONSEQUENT))
        self.assertEqual(coverageVector, coverageResult.getResultVector())

    def testMergeVector(self):
        res = RuleCoverageResult([],[], None)
        self.assertEqual(res.mergeVector([1,1,0,0,2,2], [1,1,0,0,2,2]), [1,1,0,0,2,2])
        self.assertEqual(res.mergeVector([0,0,1,1,2,1], [0,0,1,1,2,1]), [0,0,1,1,2,1])
        self.assertEqual(res.mergeVector([1,1,0,0,2,2], [0,0,1,1,2,1]), [1,1,1,1,2,3])
        self.assertEqual(res.mergeVector([1,1,0,0,2,2], [0,0,1,1,2,1]), [1,1,1,1,2,3])
        self.assertEqual(res.mergeVector([1,1,1,1,2,3], [0,0,1,1,2,1]), [1,1,1,1,2,3])
        self.assertEqual(res.mergeVector([1,1,1,1,2,3], [0,0,2,1,0,1]), [1,1,3,1,2,3])
        self.assertEqual(res.mergeVector([1,1,3,1,2,3], [1,1,3,1,2,3]), [1,1,3,1,2,3])
        self.assertEqual(res.mergeVector([1,1,3,1,2,3], [1,1,3,1,2,2]), [1,1,3,1,2,3])
        self.assertEqual(res.mergeVector(res.mergeVector([1,1,3,1,2,3], [1,1,3,1,2,3]), [1,1,3,1,2,2]), [1,1,3,1,2,3])

    def testRuleCoverProteins(self):
        rule1 = Rule("{A,B} => {C}")
        rule2 = Rule("{A,B} => {Z}")
        rule3 = Rule("{ERGA,LERG} => {XXXX}")
        rule4 = Rule("{A} => {Z}")
        rule5 = Rule("{A} => {X}")
        rule6 = Rule("{A,P} => {X}")
        rule7 = Rule("{A,B} => {D}")
        rule8 = Rule("{A,B,C} => {XX}")
        rule9 = Rule("{M} => {XX}")
        p = Protein("XXABCABCABD", ">dummy")
        cov = RuleCoverage('p', 'r', 'c', 'vector')
        
        self.assertTrue(cov.getCoverageOfRuleForProtein(p, rule1).isProteinCovered())
        self.assertTrue(cov.getCoverageOfRuleForProtein(p, rule5).isProteinCovered())
        self.assertTrue(cov.getCoverageOfRuleForProtein(p, rule7).isProteinCovered())
        self.assertTrue(cov.getCoverageOfRuleForProtein(p, rule8).isProteinCovered())

        self.assertFalse(cov.getCoverageOfRuleForProtein(p, rule4).isProteinCovered())
        self.assertFalse(cov.getCoverageOfRuleForProtein(p, rule3).isProteinCovered())
        self.assertFalse(cov.getCoverageOfRuleForProtein(p, rule2).isProteinCovered())
        self.assertFalse(cov.getCoverageOfRuleForProtein(p, rule6).isProteinCovered())
        self.assertFalse(cov.getCoverageOfRuleForProtein(p, rule9).isProteinCovered())


def main():
    unittest.main()

if __name__ == '__main__':
    main()