# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import os
from metrics import *

from sys import argv, exit

class StringMetricsTest(unittest.TestCase):
    
    def testLevenshtein(self):
        self.assertEqual(StringMetrics.levenshtein("SPLH", "TPLH"), 1)
        self.assertEqual(StringMetrics.levenshtein("ALHI", "PLHY"), 2)
        self.assertEqual(StringMetrics.levenshtein("gambol", "gumbo"), 2)
        self.assertEqual(StringMetrics.levenshtein("book", "back"), 2)
        self.assertEqual(StringMetrics.levenshtein("kitten", "sitten"), 1)
        self.assertEqual(StringMetrics.levenshtein("carro", "minuto"), 5)
        self.assertEqual(StringMetrics.levenshtein("caca", "rulo"), 4)
        self.assertEqual(StringMetrics.levenshtein("gumbo", "gambol"), 2)
        self.assertEqual(StringMetrics.levenshtein("zeil", "trials"), 4)
        self.assertEqual(StringMetrics.levenshtein("asd", ""), 3)
        self.assertEqual(StringMetrics.levenshtein("", "ccac"), 4)
        self.assertEqual(StringMetrics.levenshtein("", ""), 0)

def main():
    unittest.main()

if __name__ == '__main__':
    main()