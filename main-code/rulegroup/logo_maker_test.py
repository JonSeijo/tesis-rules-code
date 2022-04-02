# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import os
from logo_maker import *

from sys import argv, exit

class LogoMakerTest(unittest.TestCase):
	
	def testQuantityOfPositions(self):
		lg = LogoMaker(False)
		lg.readWord("SPLH")
		self.assertEqual(lg.getQuantityOfPositions(),4)

	def testEmptyPositionHasNoElements(self):
		pos = LogoPosition()
		self.assertEqual(pos.getQuantityOfLetters(), 0)


	def testAddElementToEmptyPosition(self):
		""" Check that the empty position adds a new element correctly"""
		pos = LogoPosition()
		pos.addValue("a")
		self.assertEqual(pos.getQuantityOfLetters(), 1)
		self.assertEqual(pos.getQuantityOf("a"), 1)

	def testGetQuantityOfNonExistentElementForPosition(self):
		""" Checks that a not defined letter in a positions returns 0 """
		pos = LogoPosition()
		pos.addValue("a")
		self.assertEqual(pos.getQuantityOfLetters(), 1)
		self.assertEqual(pos.getQuantityOf("b"), 0)

	def testAddElementToNonEmptyPosition(self):
		""" Check that a Position adds a new element correctly"""
		pos = LogoPosition()
		pos.addValue("a")
		pos.addValue("b")
		self.assertEqual(pos.getQuantityOfLetters(), 2)
		self.assertEqual(pos.getQuantityOf("b"), 1)
		self.assertEqual(pos.getQuantityOf("a"), 1)

	def testAddElementToNonEmptyPositionWithExistingElement(self):
		""" Check that a Position adds a new element correctly"""
		pos = LogoPosition()
		pos.addValue("a")
		pos.addValue("b")
		pos.addValue("b")
		self.assertEqual(pos.getQuantityOfLetters(), 2)
		self.assertEqual(pos.getQuantityOf("b"), 2)
		self.assertEqual(pos.getQuantityOf("a"), 1)

	def testGetQuantityOfTotalElements(self):
		""" Checks the total amount of elements in the position """
		pos = LogoPosition()
		pos.addValue("c")
		pos.addValue("d")
		pos.addValue("a")
		pos.addValue("a")
		pos.addValue("b")
		pos.addValue("b")
		pos.addValue("b")
		pos.addValue("b")
		self.assertEqual(pos.getQuantityOfElements(), 8)

	def testAddElementToNonEmptyPositionWithExistingElement(self):
		""" Check that a Position adds a new element correctly"""
		pos = LogoPosition()
		pos.addValue("c")
		pos.addValue("d")
		pos.addValue("a")
		pos.addValue("a")
		pos.addValue("b")
		pos.addValue("b")
		pos.addValue("b")
		pos.addValue("b")
		total = pos.getQuantityOfElements()
		self.assertAlmostEqual(pos.getFractionOf("d"), 0.125)
		self.assertAlmostEqual(pos.getFractionOf("c"), 0.125)
		self.assertAlmostEqual(pos.getFractionOf("a"), 0.25)
		self.assertAlmostEqual(pos.getFractionOf("b"), 0.5)

	def testWordAddedToEachPosition(self):
		""" Checks that when a word is added to the logo maker, the positions
		have the correct words """
		lg = LogoMaker(False)
		lg.readWord("SPLH")
		self.assertEqual(lg.positions[0].getQuantityOf("Z"),0)
		self.assertEqual(lg.positions[0].getQuantityOf("S"),1)
		self.assertEqual(lg.positions[1].getQuantityOf("P"),1)
		self.assertEqual(lg.positions[2].getQuantityOf("L"),1)
		self.assertEqual(lg.positions[3].getQuantityOf("H"),1)
		self.assertEqual(lg.positions[3].getQuantityOf("C"),0)

	def testAddMultipleWords(self):
		""" Checks that when multiple words are added to the logo maker, 
		the positions have the correct words """
		lg = LogoMaker(False)
		lg.readWord("SPLH")
		lg.readWord("TPLA")
		self.assertEqual(lg.positions[0].getQuantityOf("Z"),0)
		self.assertEqual(lg.positions[0].getQuantityOf("S"),1)
		self.assertEqual(lg.positions[1].getQuantityOf("P"),2)
		self.assertEqual(lg.positions[2].getQuantityOf("L"),2)
		self.assertEqual(lg.positions[3].getQuantityOf("H"),1)
		self.assertEqual(lg.positions[3].getQuantityOf("A"),1)
		self.assertEqual(lg.positions[3].getQuantityOf("C"),0)
		self.assertEqual(lg.positions[0].getQuantityOfLetters(), 2)
		self.assertEqual(lg.positions[1].getQuantityOfLetters(), 1)

	def testAddMultipleWords2(self):
		""" Checks that when multiple words are added to the logo maker, 
		the positions have the correct words """
		lg = LogoMaker(False)
		lg.readWord("SPLH")
		lg.readWord("TPLA")
		lg.readWord("MKLA")
		self.assertEqual(lg.positions[0].getQuantityOf("M"),1)
		self.assertEqual(lg.positions[0].getQuantityOf("S"),1)
		self.assertEqual(lg.positions[1].getQuantityOf("P"),2)
		self.assertEqual(lg.positions[1].getQuantityOf("K"),1)
		self.assertEqual(lg.positions[2].getQuantityOf("L"),3)
		self.assertEqual(lg.positions[3].getQuantityOf("H"),1)
		self.assertEqual(lg.positions[3].getQuantityOf("A"),2)
		self.assertEqual(lg.positions[3].getQuantityOf("C"),0)
		self.assertEqual(lg.positions[0].getQuantityOfLetters(), 3)
		self.assertEqual(lg.positions[1].getQuantityOfLetters(), 2)
		self.assertEqual(lg.positions[2].getQuantityOfLetters(), 1)
		self.assertEqual(lg.positions[3].getQuantityOfLetters(), 2)
		self.assertEqual(lg.getQuantityOfPositions(), 4)

	def testAddMultipleWordsDifferentLength(self):
		""" Checks that when multiple words are added to the logo maker, 
		the positions have the correct words """
		lg = LogoMaker(False)
		lg.readWord("SPLH")
		lg.readWord("TPLA")
		lg.readWord("MKLAG")
		self.assertEqual(lg.positions[0].getQuantityOf("M"),1)
		self.assertEqual(lg.positions[0].getQuantityOf("S"),1)
		self.assertEqual(lg.positions[1].getQuantityOf("P"),2)
		self.assertEqual(lg.positions[1].getQuantityOf("K"),1)
		self.assertEqual(lg.positions[2].getQuantityOf("L"),3)
		self.assertEqual(lg.positions[3].getQuantityOf("H"),1)
		self.assertEqual(lg.positions[3].getQuantityOf("A"),2)
		self.assertEqual(lg.positions[3].getQuantityOf("C"),0)
		self.assertEqual(lg.positions[4].getQuantityOf("A"),0)
		self.assertEqual(lg.positions[4].getQuantityOf("G"),1)

		self.assertEqual(lg.positions[0].getQuantityOfLetters(), 3)
		self.assertEqual(lg.positions[1].getQuantityOfLetters(), 2)
		self.assertEqual(lg.positions[2].getQuantityOfLetters(), 1)
		self.assertEqual(lg.positions[3].getQuantityOfLetters(), 2)
		self.assertEqual(lg.positions[4].getQuantityOfLetters(), 1)
		self.assertEqual(lg.getQuantityOfPositions(), 5)

	def testAddMultipleWords2(self):
		""" Checks that when multiple words are added to the logo maker, 
		the positions have the correct words """
		lg = LogoMaker("tests/logo-test.sto")
		self.assertEqual(lg.positions[0].getQuantityOf("T"),1)
		self.assertEqual(lg.positions[0].getQuantityOf("S"),1)
		self.assertEqual(lg.positions[1].getQuantityOf("P"),2)
		self.assertEqual(lg.positions[2].getQuantityOf("L"),2)
		self.assertEqual(lg.positions[3].getQuantityOf("H"),2)
		self.assertEqual(lg.positions[3].getQuantityOf("A"),0)
		self.assertEqual(lg.positions[0].getQuantityOfLetters(), 2)
		self.assertEqual(lg.positions[1].getQuantityOfLetters(), 1)

def main():
	unittest.main()

if __name__ == '__main__':
	main()