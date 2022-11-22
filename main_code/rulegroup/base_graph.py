# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import argparse
import re
from pathlib import Path

class Node(object):
    def __init__(self, node):
        self.node = node.strip()

    def __eq__(self, other): 
        return self.node == other.node

    def __hash__(self):
        return hash((self.node))

class GraphvizNode(Node):
    def __init__(self, node, opts):
        self.node = node
        self.edgeValue = None
        self.highlight = None
        
        if 'edgeValue' in opts:
            self.edgeValue = opts['edgeValue']

        if 'highlight' in opts:
            self.highlight = opts['highlight']

    def __eq__(self, other): 
        return self.node == other.node and self.edgeValue == other.edgeValue and self.highlight == other.highlight

    def __hash__(self):
        return hash((self.node, self.highlight, self.edgeValue))

class BaseGraph(object):
    """ Generates a graph of related items. It does not model a general graph! """

    def __init__(self, graphMode):
        """ Initialize object and set parameters """
        super(BaseGraph, self).__init__()
        self.adjacencyList = {}
        self.graphMode = graphMode
        self.nodes = set()

    def alreadyInList(self, n1, n2):
        """ Checks whether the node "n2" is in the list of adjacents to "n1" already """
        return any(x for x in self.adjacencyList[n1] if x.node == n2)

    def addNode(self, node):
        """ add a new node to the graph """
        n = Node(node)
        self.nodes.add(n)
        if node not in self.adjacencyList:
            self.adjacencyList[node] = [] 
        return n

    def addLinkInternal(self, n1, n2):
        """ Add link between nodes """
        self.addNode(n1)
        node = self.addNode(n2)
        if n1 in self.adjacencyList and not(self.alreadyInList(n1, n2)):
            #print("Adding %s to adj list" % n1)
            self.adjacencyList[n1].append(node)


    def addLink(self, n1, n2):
        """ Add link between nodes """
        self.addLinkInternal(n1, n2)
        if self.graphMode == "graph":
            self.addLinkInternal(n2, n1)
        #self.printAdjacencyList()

    def printAdjacencyList(self):
        print("Printing adjacencyList... ")
        for node,adjacents in self.adjacencyList.items():
            print("[[ %s ]] ---> " % node, end='')
            for adj in adjacents:
                print(adj.node + " ")
            print(" --- \n")


class SimpleGraph(BaseGraph):
    def __init__(self, graphMode):
        """ Initialize object and set parameters """
        super(SimpleGraph, self).__init__(graphMode)

    def markNode(self, node, visited, index, components):
        """ Mark the node as visited """
        if visited[node] == False:
            visited[node] = True
            if index in components:
                components[index].append(node)
            else:
                components[index] = [node]

            for adj in self.adjacencyList[node]:
                self.markNode(adj.node, visited, index, components)
                    

    def connectedComponents(self):
        """ Returns a dictionary of the connected components """
        visited = {}
        for n in self.nodes:
            visited[n.node] = False

        components = {}
        index = 0
        for n in self.nodes:
            if visited[n.node] == False:
                self.markNode(n.node, visited, index, components)
                index = index + 1

        return components
    
    def buildReplacementMap(self):
        """ Makes a map of node -> candidate node in the connected component to replace them if necessary """
        components = self.connectedComponents()
        replacementDictionary = {}

        totalItems = 0
        for ccid,items in components.items():
            if len(items) > 0:
                totalItems += len(items) #remove
                items.sort()
                replacementKey = items[0]
                for it in items:
                    replacementDictionary[it] = replacementKey

        #todo: remove
        if totalItems != len(self.nodes):
            raise Error("Wrong item count")
        return replacementDictionary

class GraphvizGraph(BaseGraph):
    """ Generates a graph of items and writes a dot file for visualizing the data of the graph via GraphViz """

    def __init__(self, dotFile, imageFile, graphMode, graphTitle, minAdjacents = 0):
        """ Initialize object and set parameters """
        super(GraphvizGraph, self).__init__(graphMode)
        self.dotFile = dotFile
        self.imageFile = imageFile
        self.graphTitle = graphTitle
        self.minAdjacents = minAdjacents

        if graphMode == "digraph":
            self.edgeType = "->"
        else:
            self.edgeType = "--"

    def addNode(self, node, opts = {}):
        """ add a new node to the graph """
        n = GraphvizNode(node, opts)
        self.nodes.add(n)
        if node not in self.adjacencyList:
            self.adjacencyList[node] = [] 
        return n

    def addLinkInternal(self, n1, n2, opts = {}):
        """ Add link between nodes """
        self.addNode(n1, opts)
        node = self.addNode(n2, opts)
        if n1 in self.adjacencyList and not(self.alreadyInList(n1, n2)):
            self.adjacencyList[n1].append(node)

    def addLink(self, n1, n2, opts = {}):
        """ Add link between nodes. Override default behavior for graphviz in order to avoid duplicate edges when using graphs"""
        self.addLinkInternal(n1, n2, opts)

    def generateGraphvizFile(self):
        """ Generate a dot file based on the rules of the items and how they are related (antecedents -> consequents) """
        with open(self.dotFile, 'w') as outfile:
            outfile.write(self.graphMode+" world {\n")

            for node,adjacents in self.adjacencyList.items():
                if len(adjacents) >= self.minAdjacents:
                    if len(adjacents) > 0:
                        for adj in adjacents:
                            highlightFormat = ""
                            edgeValue = ""
                            try:
                                if adj.highlight:
                                    highlightFormat = ", color=\"red\""
                            except:
                                pass

                            try:                            
                                if adj.edgeValue:
                                    edgeValue = str(adj.edgeValue)
                            except:
                                pass

                            outfile.write("\t%s %s %s [label=\"%s\" %s ];\n"  %(node, self.edgeType, adj.node, edgeValue, highlightFormat))
                    else:
                        outfile.write("\t%s;\n"  %(node))

            outfile.write('label = "\n%s";' % self.graphTitle)
            outfile.write("}")
            outfile.close()

    def graph(self):
        """ Make a system call for the dot program and send the dot file in order to generate the implication graph """
        self.generateGraphvizFile()
        os.system("dot -Tpng " + self.dotFile + " -o " + self.imageFile)
