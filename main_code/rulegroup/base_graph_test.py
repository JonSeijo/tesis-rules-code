# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import os
import re
from base_graph import BaseGraph, Node, SimpleGraph, GraphvizGraph

class BaseGraphTest(unittest.TestCase):
    
    def testAddNode(self):
        g = BaseGraph("digraph")
        g.addNode("holi")

        node = Node("holi")
        nodes = set()
        nodes.add(node)
        self.assertEqual(g.nodes, nodes)

    def testAddLinkBetweenNodesAndCheckNodesAreAdded(self):
        g = SimpleGraph("graph")
        g.addLink("holi", "chau")

        node = Node("holi")
        node2 = Node("chau")
        nodes = set()
        nodes.add(node)
        nodes.add(node2)
        self.assertEqual(g.nodes, nodes)

    def testAddLinkBetweenNodesHasTheCorrespondingEdges(self):
        g = SimpleGraph("graph")
        g.addLink("holi", "chau")
        
        self.assertEqual(g.adjacencyList["holi"][0], Node("chau"))
        self.assertEqual(g.adjacencyList["chau"][0], Node("holi"))

    def testCheckThatNoSpuriousLinksAreAdded(self):
        g = SimpleGraph("graph")
        g.addLink("holi", "chau")
        g.addLink("chau", "mmmm")
        
        self.assertEqual(len(g.adjacencyList["holi"]), 1)
        self.assertEqual(len(g.adjacencyList["mmmm"]), 1)
        self.assertEqual(len(g.adjacencyList["chau"]), 2)

    def testVerticesOfExample(self):
        g = self.exampleGraph()
        nodes = set()
        l = ["ELLL", "RLLL", "KLLL", "TALM", "TALH", "TPLH",
        "SPLH", "IVKL", "VVKL", "ADIN", "ADVN", "ADPN", "ANVN"]
        for e in l:
            nodes.add(Node(e))

        self.assertEqual(g.nodes, nodes)

    def testCountConnectedComponents(self):
        g = self.exampleGraph()
        self.assertEqual(len(g.connectedComponents().keys()), 4)

    def testConnectedComponents(self):
        g = self.exampleGraph()
        components = g.connectedComponents()

        result = set()
        expected = set()
        expected.add(frozenset(["ELLL", "RLLL", "KLLL"]))
        expected.add(frozenset(["IVKL", "VVKL"]))
        expected.add(frozenset(["TALM", "TALH", "TPLH", "SPLH"]))
        expected.add(frozenset(["ADIN", "ADVN", "ADPN", "ANVN"]))
        
        for key, items in components.items():
            result.add(frozenset(items))

        self.assertEqual(expected, result)

    def testConnectedComponents2(self):
        g = SimpleGraph("graph")
        g.addLink("holi", "chau")

        components = g.connectedComponents()
        result = set()
        expected = set()
        expected.add(frozenset(["holi", "chau"]))
        for key, items in components.items():
            result.add(frozenset(items))

        self.assertEqual(result, expected)

    def testReplacementDictionary(self):
        g = self.exampleGraph()
        expected = {
            "KLLL" : "ELLL",
            "RLLL" : "ELLL",
            "ELLL" : "ELLL",
            "TALM" : "SPLH",
            "TPLH" : "SPLH",
            "SPLH" : "SPLH",
            "TALH" : "SPLH",
            "ADIN" : "ADIN",
            "ADVN" : "ADIN",
            "ADPN" : "ADIN",
            "ANVN" : "ADIN",
            "IVKL" : "IVKL",
            "VVKL" : "IVKL",
        }

        #print(g.buildReplacementDictionary())
        self.assertEqual(expected, g.buildReplacementMap())

    def testReplacementDictionary2(self):
        g = self.exampleGraph()
        self.assertEqual(len(g.nodes), len(g.buildReplacementMap().keys()))

    def testGraphExample(self):
        g = GraphvizGraph("tests/graph_example.dot", "tests/graph_example.png", "graph", "Ejemplo1")
         #First component
        g.addLink("ELLL", "RLLL")
        g.addLink("ELLL", "KLLL")
        g.addLink("RLLL", "KLLL")

        #Second component
        g.addLink("TALM", "TALH")
        g.addLink("TALH", "TPLH")
        g.addLink("TPLH", "SPLH")

        #Third component
        g.addLink("IVKL", "VVKL")

        #Fourth component
        g.addLink("ADIN", "ADVN")
        g.addLink("ADIN", "ADPN")
        g.addLink("ADVN", "ADPN")
        g.addLink("ADVN", "ANVN")
        g.graph()

    def exampleGraph(self):
        g = SimpleGraph("graph")
        
        #First component
        g.addLink("ELLL", "RLLL")
        g.addLink("ELLL", "KLLL")
        g.addLink("RLLL", "KLLL")

        #Second component
        g.addLink("TALM", "TALH")
        g.addLink("TALH", "TPLH")
        g.addLink("TPLH", "SPLH")

        #Third component
        g.addLink("IVKL", "VVKL")

        #Fourth component
        g.addLink("ADIN", "ADVN")
        g.addLink("ADIN", "ADPN")
        g.addLink("ADVN", "ADPN")
        g.addLink("ADVN", "ANVN")

        return g


def main():
    unittest.main()

if __name__ == '__main__':
    main()