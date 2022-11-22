# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import argparse
import re
import statistics
from pathlib import Path
from fastaread import Protein,FastaParser

class ProteinStats(object):
    """ Calculate stats (length statistics) of the protein family and its aminoacid distribution """

    def __init__(self, proteinPath, proteinFile):
        """ Parse parameters and initialize object """
        self.proteinPath = proteinPath
        self.proteinFile = proteinFile
        self.proteins = []
        self.stats = {}
        
    def readProteinsFromFile(self):
        """ Read proteins from a list """
        fp = FastaParser()
        with open(self.proteinFile, 'r') as pfile:
            for line in pfile:
                fp.readFile(line.strip())
                for protein in fp.getProteins():
                    self.proteins.append(protein.getEncoding())
    

    def readProteinsFromPath(self):
        """ Read the proteins from the path and store them """
        fp = FastaParser()
        for filename in os.listdir(self.proteinPath):
            fp.readFile(self.proteinPath+filename.strip())
            for protein in fp.getProteins():
                self.proteins.append(protein.getEncoding())

        print("Read %s proteins." % (str(len(self.proteins))))


    def getStats(self, proteinList):
        """ Get a summary of stats for the proteins in the list """
        lenghts = [len(x) for x in proteinList]
        self.stats['#Proteins'] = len(proteinList)
        self.stats['Length - Mean'] = statistics.mean(lenghts)
        self.stats['Length - Median'] = statistics.median(lenghts)
        self.stats['Length - Std Dev'] = statistics.stdev(lenghts)
        totalLength = sum(lenghts)

        self.aminoacids = {}
        for protein in proteinList:
            for aminoacid in protein:
                if aminoacid in self.aminoacids:
                    self.aminoacids[aminoacid] += 1
                else:
                    self.aminoacids[aminoacid] = 1

        for k,v in self.aminoacids.items():
            self.aminoacids[k] = float(v)/float(totalLength)




    def process(self):
        """ Process the protein file and display the stats in the console """
        if self.proteinPath != None and len(self.proteinPath) > 0:
            self.readProteinsFromPath()
        elif self.proteinFile != None and len(self.proteinFile) > 0:
            self.readProteinsFromFile()

        self.getStats(self.proteins)

        print(" General\n")
        for key,value in self.stats.items():
            print(" %s: %s" % (str(key), str(value)))

        print("\n\n Aminoacids distribution\n")
        for key,value in self.aminoacids.items():
            print(" %s: %s" % (str(key), str(value)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proteinPath", help="The path that contains the proteins to be analized.", default=None)
    parser.add_argument("--proteinFile", help="The list of proteins to be analized.", default=None)

    args = parser.parse_args()

    ps = ProteinStats(args.proteinPath, args.proteinFile)
    ps.process()

if __name__ == "__main__":
    # execute only if run as a script
    main()