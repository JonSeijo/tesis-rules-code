# -*- coding: utf-8 -*-
#!/usr/bin/python
#

import os
import re
import argparse
from pathlib import Path
import random
import math
import operator

class LogoMaker(object):
    """ Parses a .sto file and makes an html logo """

    CONTAINER_HEIGHT = 420
    COLORS = ["Red", "Blue", "BlueViolet", "Brown", "BurlyWood", "CadetBlue", "Chartreuse", "Chocolate", 
    "SlateGrey", "RoyalBlue", "Crimson", "Black", "Navy",
    "DarkSlateBlue ", "ForestGreen", "Fuchsia", "LightGreen", "DarkViolet", "GoldenRod", "Gold", "LightPink", "Tomato", "YellowGreen"]


    def __init__(self, inputFilename):
        """ Creates an instance of the class for reading and initializes the input file attribute """
        self.input = inputFilename
        self.positions = []
        if self.input != False:
            self.processFile()

    def getQuantityOfPositions(self):
        """ Returns the quantity of positions for the logo word """
        return len(self.positions)

    def readWord(self, word):
        """ Reads a word and stores the positions accordingly """
        m = 0
        for i in range(0, self.getQuantityOfPositions()):
            m = m+1
            self.positions[i].addValue(word[i])

        if len(word) > m:
            #There are elements in the word not checked
            for i in range(m, len(word)):
                newPosition = LogoPosition()
                newPosition.addValue(word[i])
                self.positions.append(newPosition)


    def processFile(self):
        """ Reads the file received and process each line creating words """
        with open(self.input, 'r') as infile:
            for line in infile:
                l = line.strip()
                if len(l) > 0 and (l[0] != '#' or l[0] != '//'): #Skip comments or file ending mark
                    parts = re.split(r'\t+', l)
                    if len(parts) > 1:
                        self.readWord(parts[1]) #Discard the filename and keep the words

    def openFile(self):
        contents = """ 
        <!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  </head>
  <body>
"""
        return contents + "<svg style=\"padding: 10px;\" height=\""+ str(self.CONTAINER_HEIGHT) +"\" width=\""+ str(self.getQuantityOfPositions()*math.floor(self.CONTAINER_HEIGHT*0.65)) +"\">"

    def closeFile(self):
        return "</svg></body></html>"

    def writeTag(self, content, x, y, color, height):
        return "<text style=\"font-family: monospace; font-size:"+str(height)+"px;\" x=\""+str(x)+"\" y=\""+str(y)+"\" fill=\""+color+"\">"+ content +"</text>"

    def graphPositions(self):
        """ Graph the positions drawing each tag """
        content = ""
        x = 0
        for pos in self.positions:
            y = 0
            posSorted = sorted(pos.letterCount.items(), key=operator.itemgetter(1), reverse=False)
            maxWidth = 1

            for letter in posSorted:
            #for letter in pos.letterCount:
                containerHeight = math.floor(self.CONTAINER_HEIGHT*pos.getFractionOf(letter[0])*0.95)
                currentWidth = math.floor(containerHeight*0.66)
                if currentWidth > maxWidth:
                    maxWidth = currentWidth


            for letter in posSorted:
            #for letter in pos.letterCount:
                color = self.COLORS[random.randint(0, len(self.COLORS)-1)]
                containerHeight = math.floor(self.CONTAINER_HEIGHT*pos.getFractionOf(letter[0])*0.95)
                content = content + self.writeTag(letter[0], x, math.floor((self.CONTAINER_HEIGHT-y)), color, math.floor(containerHeight*0.95))
                y = math.floor(y + containerHeight*0.70)

            x = x + maxWidth

        return content


    def makeLogo(self, outputFile):
        fileContents = self.openFile()
        fileContents = fileContents + self.graphPositions()
        fileContents = fileContents + self.closeFile()

        with open(outputFile, 'w') as outfile:
            outfile.write(fileContents)
            outfile.close()


class LogoPosition(object):

    def __init__(self):
        """ Initialize the word count dictionary """
        self.letterCount = {}

    def getQuantityOfLetters(self):
        return len(self.letterCount)

    def getQuantityOfElements(self):
        """ Returns the total amount of items in the position """
        total = 0
        for letter,count in self.letterCount.items():
            total = total + count
        return total

    def addValue(self, letter):
        """ Adds a value for the letter selected """
        if letter in self.letterCount:
            self.letterCount[letter] = self.letterCount[letter] + 1
        else:
            self.letterCount[letter] = 1

    def getQuantityOf(self, letter):
        """ Returns the quantity of letters in the current position """
        if letter not in self.letterCount:
            return 0
        else:
            return self.letterCount[letter]

    def getFractionOf(self, letter):
        """ Returns the quantity of letters in the current position """
        if letter not in self.letterCount:
            return 0
        else:
            return self.letterCount[letter]/self.getQuantityOfElements()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="The input filename to where to extract the data")
    args = parser.parse_args()

    inputFile = args.inputFile
    lm = LogoMaker(inputFile)
    lm.makeLogo(inputFile.replace(".sto", ".html"))


if __name__ == "__main__":
    # execute only if run as a script
    main()