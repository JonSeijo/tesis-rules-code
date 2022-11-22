# -*- coding: utf-8 -*-
#!/usr/bin/python

from abc import ABC,abstractmethod
from PIL import Image

class RuleCoverageExport(ABC):
    """ Abstract class that models exporters """
    def __init__(self, outfile):
        self.outfile = outfile

    @abstractmethod
    def addData(self, vector, index, proteinStr, proteinFilename, extraData = None):
        """ Add data to the internal data structures for exporting coverage results """
        pass

    @abstractmethod
    def export(self, extraData = None):
        """ Write data to a file """
        pass

class RuleCoverageExportToImage(RuleCoverageExport):
    """ Export results to a png image """

    COLOR_EMPTY = (128,128,128)
    COLOR_ANTECEDENT = (0,0,255)
    COLOR_CONSEQUENT = (255,0,0)
    COLOR_A_AND_C = (0,255,0)
    COLOR_NOTHING = (255,255,255)
    COLOR_SEPARATOR = (255,255,0)

    COLORS = [COLOR_EMPTY, COLOR_ANTECEDENT, COLOR_CONSEQUENT, COLOR_A_AND_C]

    PROTEIN_HEIGHT = 20

    def __init__(self, outfile):
        self.outfile = outfile
        self.data = []
        self.height = 0
        self.width = 0


    def addData(self, vector, index, proteinStr, proteinFilename, extraData = None):
        if len(vector) > self.width:
            self.width = len(vector)

        row = []
        for value in vector:
            row.append(self.COLORS[value])

        for i in range(0, self.PROTEIN_HEIGHT):
            self.height += 1
            self.data.append(row)

        for i in range(0, 1):
            self.data.append([self.COLOR_SEPARATOR for x in row])
            self.height += 1

    def padRows(self):
        for h in range(0, self.height):
            rowLength = len(self.data[h])
            for w in range(0, self.width - rowLength):
                self.data[h].append(self.COLOR_NOTHING)

    def export(self, extraData = None):
        self.padRows()
        img = Image.new('RGB', (self.width, self.height))
        data = [item for sublist in self.data for item in sublist]
        img.putdata(data)
        img.save(self.outfile)


class RuleCoverageExportToVector(RuleCoverageExport):
    """ Write coverage result ot a vector """

    def __init__(self, outfile):
        self.outfile = outfile
        self.file = open(outfile, 'w')

    def __del__(self):
        self.file.close()

    def addData(self, vector, index, proteinStr, proteinFilename, extraData = None):
        self.file.write(' '.join(str(x) for x in vector) + "\n")

    def export(self, extraData = None):
        pass
                        

class RuleCoverageExportToXYZ(RuleCoverageExport):
    """ Write coverage result in other vector format """

    def __init__(self, outfile):
        self.outfile = outfile
        self.file = open(outfile, 'w')

    def __del__(self):
        self.file.close()

    def addData(self, vector, index, proteinStr, proteinFilename, extraData = None):
        for x in range(0, len(vector)):
            self.file.write(str(x) + " " + str(index) + " " + str(vector[x]) + "\n")

    def export(self, extraData = None):
        pass

class RuleCoverageExportToHtml(RuleCoverageExport):
    """ Export results to html with each protein and the coverage result """

    COLOR_EMPTY = '#AAAAAA'
    COLOR_ANTECEDENT = '#0000FF'
    COLOR_CONSEQUENT = '#FF0000'
    COLOR_A_AND_C = "#00FF00"

    COLORS = [COLOR_EMPTY, COLOR_ANTECEDENT, COLOR_CONSEQUENT, COLOR_A_AND_C]

    def __init__(self, outfile):
        self.outfile = outfile
        self.file = open(outfile, 'w')
        self.beginFile()

    def __del__(self):
        self.file.close()

    def writeCharacter(self, character, code):
        if code > 0:
            return '<span style="color:'+self.COLORS[code]+';">'+character+"</span>"
        else: 
            return character

    def addData(self, vector, index, proteinStr, proteinFilename, extraData = None):
        if extraData is not None and 'proteinFraction' in extraData.keys():
            self.file.write("<span style=\"color: #333;\"> %s - Coverage: %s</span><br/>" % (proteinFilename.strip(), str(extraData['proteinFraction'])))
        else:
            self.file.write("%s - " % proteinFilename)

        for i in range(0, len(proteinStr)):
            self.file.write(self.writeCharacter(proteinStr[i], vector[i]))

        self.file.write('</br></br>')

    def export(self, extraData = None):
        if extraData is not None and 'covered' in extraData.keys() and 'total' in extraData.keys():
            self.file.write("<span style=\"color: #333;\"> Total Coverage: %s</span>" % str(extraData['covered']/extraData['total']))
        self.endFile()

    def beginFile(self):
        self.file.write("<html><head><style>body { color: #AAAAAA; font-family: Courier, 'Lucida Console', monospace; font-size: 12px; }</style></head><body>")

    def endFile(self):
        self.file.write("</body></html>")

class RuleCoverageExportToCsv(RuleCoverageExport):
    """ Export data to CSV format """
    
    def __init__(self, outfile):
        self.outfile = outfile
        self.file = open(outfile, 'w')

    def __del__(self):
        self.file.close()

    def addData(self, vector, index, proteinStr, proteinFilename, extraData = None):
        self.file.write("%s," % proteinFilename.strip())
        if extraData is not None and 'proteinFraction' in extraData.keys():
            self.file.write("%s," % str(extraData['proteinFraction']))

        self.file.write("%s" % proteinStr)
        self.file.write('\n')

    def export(self, extraData = None):
        if extraData is not None and 'covered' in extraData.keys() and 'total' in extraData.keys():
            self.file.write("Total Coverage,%s" % str(extraData['covered']/extraData['total']))


class RuleByTypeCoverageExportToImage(RuleCoverageExportToImage):
    """ Export results to a png image """
    COLOR_EMPTY = (128,128,128)
    COLOR_ANTECEDENT_1 = (0,0,255)
    COLOR_CONSEQUENT_1 = (255,0,0)
    COLOR_A_AND_C_1 = (0,255,0)

    COLOR_ANTECEDENT_2 = (238,148,51)
    COLOR_CONSEQUENT_2 = (153,84,151)
    COLOR_A_AND_C_2 = (108,153,84)

    COLOR_ANTECEDENT_3 = (77,140,204)
    COLOR_CONSEQUENT_3 = (156,77,204)
    COLOR_A_AND_C_3 = (145,204,167)

    COLOR_NOTHING = (255,255,255)
    COLOR_SEPARATOR = (238,226,132)

    COLORS = {
        1:[COLOR_EMPTY, COLOR_ANTECEDENT_1, COLOR_CONSEQUENT_1, COLOR_A_AND_C_1],
        2:[COLOR_EMPTY, COLOR_ANTECEDENT_1, COLOR_CONSEQUENT_1, COLOR_A_AND_C_1],
        3:[COLOR_EMPTY, COLOR_ANTECEDENT_1, COLOR_CONSEQUENT_1, COLOR_A_AND_C_1],
    }

    PROTEIN_HEIGHT = 15

    def __init__(self, outfile):
        self.outfile = outfile
        self.data = []
        self.height = 0
        self.width = 0


    def addData(self, vector, index, proteinStr, proteinFilename, extraData, ruleType):
        """ Add data by rule type. Selecting different palletes according to the rule type. And add an extra separator per protein analyzed"""
        if len(vector) > self.width:
            self.width = len(vector)

        row = []
        for value in vector:
            row.append(self.COLORS[ruleType][value])

        for i in range(0, self.PROTEIN_HEIGHT):
            self.height += 1
            self.data.append(row)

        for i in range(0, 1):
            self.data.append([self.COLOR_SEPARATOR for x in row])
            self.height += 1

    def addExtraSeparation(self):

        row = [self.COLOR_NOTHING for x in range(0, self.width)]

        for i in range(0, 5):
            self.data.append(row)
            self.height += 1