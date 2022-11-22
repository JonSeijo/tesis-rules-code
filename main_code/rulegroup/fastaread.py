# -*- coding: utf-8 -*-
#!/usr/bin/python
#

import os
import argparse
from pathlib import Path

class Protein(object):
	""" Models a protein with the data parsed from a fasta file. """

	def __init__(self, encoding, comment, filename = ''):
		self.encoding = encoding
		self.comment = comment
		self.filename = filename

	def getLength(self):
		""" Returns the length of the protein """
		return len(self.encoding)

	def getEncoding(self):
		""" Returns the representation of the protein """
		return self.encoding

	def getComment(self):
		""" Returns the comment of the fasta file that belongs to the protein """
		return self.comment

	def getFilename(self):
		""" Returns the filename of the fasta file parsed """
		return self.filename


class FastaParser(object):
	""" Utility for parsing fasta files into proteins """

	def __init__(self):
		self.proteins = []
	
	def getProteins(self):
		""" Return the parsed proteins """
		return self.proteins

	def getProtein(self, index = 0):
		""" Return the protein identified by index """
		return self.proteins[index]

	def pushProtein(self, encoding, comment, filename = ''):
		""" Push and create a protein to the protein dictionary from the received parameters """
		p = Protein(encoding, comment, filename)
		self.proteins.append(p)

	def readFile(self, inputFile):
		""" Read file line by line getting the proteins stored """
		self.proteins = []
		with open(inputFile, 'r') as infile:
			comment = ''
			encoding = ''

			for line in infile:
				l = line.strip()
				if l[0] == '>':
					if len(comment) > 0:
						#Then I'm reading another protein in the file (multifasta)
						self.pushProtein(encoding, comment, inputFile)
						encoding = ''
						comment = ''
					comment = l
				else:
					encoding += l

			self.pushProtein(encoding, comment, inputFile)
				

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("inputFile", help="The input filename to where to the proteins (FASTA format)")
	args = parser.parse_args()

	rg = FastaParser()
	rg.readFile(args.inputFile)


if __name__ == "__main__":
    # execute only if run as a script
    main()