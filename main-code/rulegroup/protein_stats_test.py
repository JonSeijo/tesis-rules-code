# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import os
import re
from fastaread import Protein,FastaParser
from protein_stats import ProteinStats
from sys import argv, exit


class ProteinStatsTest(unittest.TestCase):
    
    def testSummaryOfProtein(self):
        proteins = ["AACCBB", "AACCBB"]
        ps = ProteinStats("lalala", "hola")
        ps.getStats(proteins)

        self.assertEqual(ps.stats['#Proteins'],  len(proteins))
        self.assertEqual(ps.stats['Length - Mean'],  6)
        self.assertEqual(ps.stats['Length - Median'],  6)
        self.assertEqual(ps.stats['Length - Std Dev'],  0)

    def testSummaryOfProtein2(self):
        proteins = ["AACCBB", "A"]
        ps = ProteinStats("lalala", "hola")
        ps.getStats(proteins)

        self.assertAlmostEqual(ps.stats['#Proteins'],  len(proteins))
        self.assertAlmostEqual(ps.stats['Length - Mean'],  3.5)
        self.assertAlmostEqual(ps.stats['Length - Median'],  3.5)
        self.assertAlmostEqual(ps.stats['Length - Std Dev'],  3.5355339)


    def testSummaryOfProtein3(self):
        proteins = ["AACCBB", "A", "AAD", "CMAMCADAFASASD", "AAA3AFC", "ASDALKDJAL"]
        ps = ProteinStats("lalala", "hola")
        ps.getStats(proteins)

        self.assertAlmostEqual(ps.stats['#Proteins'],  len(proteins))
        self.assertAlmostEqual(ps.stats['Length - Mean'],  6.8333333)
        self.assertAlmostEqual(ps.stats['Length - Median'],  6.5)
        self.assertAlmostEqual(ps.stats['Length - Std Dev'],  4.70814896394184)


    def testAminoacidsFrequency1(self):
        proteins = ["AACCBB", "AACCBB"]
        ps = ProteinStats("lalala", "hola")
        ps.getStats(proteins)
        self.assertAlmostEqual(ps.aminoacids['A'], 1.0/3.0)
        self.assertAlmostEqual(ps.aminoacids['C'], 1.0/3.0)
        self.assertAlmostEqual(ps.aminoacids['B'], 1.0/3.0)

    def testAminoacidsFrequency2(self):
        proteins = ["AACCBB", "A"]
        ps = ProteinStats("lalala", "hola")
        ps.getStats(proteins)

        self.assertAlmostEqual(ps.aminoacids['A'], 3.0/7.0)
        self.assertAlmostEqual(ps.aminoacids['C'], 2.0/7.0)

    def testAminoacidsFrequency3(self):
        proteins = ["AACCBB", "A", "AAD", "CMAMCADAFASASD", "AAA3AFC", "ASDALKDJAL"]
        ps = ProteinStats("lalala", "hola")
        ps.getStats(proteins)

        self.assertAlmostEqual(ps.aminoacids['A'], 17.0/41.0)
        self.assertAlmostEqual(ps.aminoacids['L'], 2.0/41.0)

    def testOpenProfeinFile(self):
        proteins = ["SDLGKKLLEAARAGQDDEVRILMANGADVNAEDKVGLTPLHLAAMNDHLEIVEVLLKNGADVNAIDAIGETPLHLVAMYGHLEIVEVLLKHGADVNAQDKFGKTAFDISIDNGNEDLAEILQKL"]
        ps = ProteinStats("lalala", "tests/pfile2.txt")
        ps.readProteinsFromFile()
        self.assertEqual(proteins, ps.proteins)

def main():
    unittest.main()

if __name__ == '__main__':
    main()