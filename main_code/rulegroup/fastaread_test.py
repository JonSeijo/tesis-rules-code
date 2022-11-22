# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import os
from fastaread import *

from sys import argv, exit


class FastaParserTest(unittest.TestCase):
    
    def testProteinDescriptionReadOk(self):
        fp = FastaParser()
        fp.readFile("tests/p2.fasta")
        comment = ">DARPIN_AR_3A mol:protein length:155"
        self.assertEqual(comment, fp.getProtein().getComment())

    def testProteinEncodingReadOk(self):
        fp = FastaParser()
        fp.readFile("tests/p2.fasta")
        protein = "SDLGKKLLEAARAGQDDEVRILMANGADVNANDWFGITPLHLVVNNGHLEIIEVLLKYAADVNASDKSGWTPLHLAAYRGHLEIVEVLLKYGADVNAMDYQGYTPLHLAAEDGHLEIVEVLLKYGADVNAQDKFGKTAFDISIDNGNEDLAEILQ"
        self.assertEqual(protein, fp.getProtein().getEncoding())
        self.assertEqual(155, fp.getProtein().getLength())

    def testProteinDescriptionReadOk2(self):
        fp = FastaParser()
        fp.readFile("tests/p1.fasta")
        comment = ">DARPIN_20 mol:protein length:124"
        self.assertEqual(comment, fp.getProtein().getComment())

    def testProteinEncodingReadOk2(self):
        fp = FastaParser()
        fp.readFile("tests/p1.fasta")
        protein = "SDLGKKLLEAARAGQDDEVRILMANGADVNAEDKVGLTPLHLAAMNDHLEIVEVLLKNGADVNAIDAIGETPLHLVAMYGHLEIVEVLLKHGADVNAQDKFGKTAFDISIDNGNEDLAEILQKL"
        self.assertEqual(protein, fp.getProtein().getEncoding())
        self.assertEqual(124, fp.getProtein().getLength())
        self.assertEqual("tests/p1.fasta", fp.getProtein().getFilename())

    def testGetListOfProteinsRead(self):
        fp = FastaParser()
        fp.readFile("tests/p1.fasta")
        comment = ">DARPIN_20 mol:protein length:124"
        protein = "SDLGKKLLEAARAGQDDEVRILMANGADVNAEDKVGLTPLHLAAMNDHLEIVEVLLKNGADVNAIDAIGETPLHLVAMYGHLEIVEVLLKHGADVNAQDKFGKTAFDISIDNGNEDLAEILQKL"
        proteins = fp.getProteins()
        self.assertEqual(1, len(proteins))
        self.assertEqual(proteins[0].getEncoding(), protein)
        self.assertEqual(proteins[0].getComment(), comment)

    def testReadMultiFastaFileEncodings(self):
        fp = FastaParser()
        fp.readFile("tests/multi.fasta")
        
        protein1 = "ACTCCCCGTGCGCGCCCGGCCCGTAGCGTCCTCGTCGCCGCCCCTCGTCTCGCAGCCGCAGCCCGCGTGGACGCTCTCGCCTGAGCGCCGCGGACTAGCCCGGGTGGCC"
        protein2 = "CAGTCCGGCAGCGCCGGGGTTAAGCGGCCCAAGTAAACGTAGCGCAGCGATCGGCGCCGGAGATTCGCGAACCCGACACTCCGCGCCGCCCGCCGGCCAGGACCCGCGGCGCGATCGCGGCGCCGCGCTACAGCCAGCCTCACTGGCGCGCGGGCGAGCGCACGGGCGCTC"
        protein3 = "CACGACAGGCCCGCTGAGGCTTGTGCCAGACCTTGGAAACCTCAGGTATATACCTTTCCAGACGCGGGATCTCCCCTCCCC"
        protein4 = "CAGCAGACATCTGAATGAAGAAGAGGGTGCCAGCGGGTATGAGGAGTGCATTATCGTTAATGGGAACTTCAGTGACCAGTCCTCAGACACGAAGGATGCTCCCTCACCCCCAGTCTTGGAGGCAATCTGCACAGAGCCAGTCTGCACACC"

        proteins = fp.getProteins()

        self.assertEqual(4, len(proteins))
        self.assertEqual(proteins[0].getEncoding(), protein1)
        self.assertEqual(proteins[1].getEncoding(), protein2)
        self.assertEqual(proteins[2].getEncoding(), protein3)
        self.assertEqual(proteins[3].getEncoding(), protein4)

    def testReadMultiFastaFileComments(self):
        fp = FastaParser()
        fp.readFile("tests/multi.fasta")
        comment1 = ">sequence1";
        comment2 = ">sequence2";
        comment3 = ">sequence3";
        comment4 = ">sequence4";

        proteins = fp.getProteins()
        self.assertEqual(4, len(proteins))
        self.assertEqual(proteins[0].getComment(), comment1)
        self.assertEqual(proteins[1].getComment(), comment2)
        self.assertEqual(proteins[2].getComment(), comment3)
        self.assertEqual(proteins[3].getComment(), comment4)

    def readFile(self, ruta):
        if not os.path.exists(ruta):
            sys.exit("El archivo '%s' no existe." % ruta)
        elif not os.path.isfile(ruta):
            sys.exit("El archivo '%s' es invalido." % ruta)

        archivo = open(ruta, "r")
        return archivo.read()



def main():
    unittest.main()

if __name__ == '__main__':
    main()