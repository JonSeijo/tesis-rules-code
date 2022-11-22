# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import os
from graph import *

from sys import argv, exit

class RuleGraphTest(unittest.TestCase):
    
    def testFrequencyInProteins(self):
        g = RuleGraph("rulefile", 3)
        
        protein1 = "ACTCCCCGTGCGCGCCCGGCCCGTAGCGTCCTCGTCGCCGCCCCTCGTCTCGCAGCCGCAGCCCGCGTGGACGCTCTCGCCTGAGCGCCGCGGACTAGCCCGGGTGGCC"
        protein2 = "CAGTCCGGCAGCGCCGGGGTTAAGCGGCCCAAGTAAACGTAGCGCAGCGATCGGCGCCGGAGATTCGCGAACCCGACACTCCGCGCCGCCCGCCGGCCAGGACCCGCGGCGCGATCGCGGCGCCGCGCTACAGCCAGCCTCACTGGCGCGCGGGCGAGCGCACGGGCGCTC"
        protein3 = "CACGACAGGCCCGCTGAGGCTTGTGCCAGACCTTGGAAACCTCAGGTATATACCTTTCCAGACGCGGGATCTCCCCTCCCC"
        protein4 = "CAGCAGACATCTGAATGAAGAAGAGGGTGCCAGCGGGTATGAGGAGTGCATTATCGTTAATGGGAACTTCAGTGACCAGTCCTCAGACACGAAGGATGCTCCCTCACCCCCAGTCTTGGAGGCAATCTGCACAGAGCCAGTCTGCACACC"

        g.proteins = [protein1, protein2, protein3, protein4]

        self.assertAlmostEqual(g.frequencyInProteins("GTC", "GTC"), 0.75)
        self.assertAlmostEqual(g.frequencyInProteins("GTC", "GCA"), 0.75)
        self.assertAlmostEqual(g.frequencyInProteins("TTC", "CCCC"), 0.50)
        self.assertAlmostEqual(g.frequencyInProteins("TTC", "CCCC"), 0.50)
        self.assertAlmostEqual(g.frequencyInProteins("AAGA", "TTCA"), 0.25)
        self.assertAlmostEqual(g.frequencyInProteins("AAGA", "TTCAC"), 0)
        self.assertAlmostEqual(g.frequencyInProteins("GG", "GG"), 1)
        self.assertAlmostEqual(g.frequencyInProteins("GAEG", "RRG"), 0)

def main():
    unittest.main()

if __name__ == '__main__':
    main()