import unittest
import pathlib
import pandas as pd

import compare_rules as cr

class TestRuleComparison(unittest.TestCase):

    def test_build_itemset(self):
        result = cr.build_itemset("{GNTA,HLAA,NTAL,PLHL}")
        expected = set(["GNTA", "HLAA", "NTAL", "PLHL"])
        self.assertEqual(expected, result)

        with self.assertRaises(cr.RuleBuildException):
            cr.build_itemset("GNTA,HLAA,NTAL,PLHL")


    def test_rule_from_str(self):
        # "{ALHV,LHIA} => {LHVA}"  ----> ({ALHV,LHIA}, {LHVA})
        result = cr.rule_from_str("{ALHV,LHIA} => {LHVA}")
        expected = (set(["ALHV", "LHIA"]), set(["LHVA"]))
        self.assertEqual(expected, result)

        with self.assertRaises(cr.RuleBuildException):
            cr.rule_from_str("{ALHV,LHIA},{LHVA}")

        with self.assertRaises(cr.RuleBuildException):
            cr.rule_from_str("{ALHV,LHIA} => ")

    def test_interseccion_base(self):
        self.assertEqual([1], cr.list_intersection([1, 2, 3], [1, 4, 5]))
        self.assertEqual([], cr.list_intersection([1, 2, 3], [4, 5, 6]))
        self.assertEqual([], cr.list_intersection([1, 2, 3], []))
        self.assertEqual([], cr.list_intersection([], [4, 5, 6]))
        self.assertEqual(["hola"], cr.list_intersection(["hola", "como", "estas"], ["hola", "komo", "estaz"]))

    def test_rules_intersection(self):
        result = cr.rules_intersection_exact(
            [   cr.rule_from_str("{HOLA,COMO} => {ESTA}"),
                cr.rule_from_str("{ESTO,NOOO} => {ESTA}")],

            [   cr.rule_from_str("{COMO,HOLA} => {ESTA}")])

        # No importa el orden, la regla debe ser la misma en el build
        expected_1 = [cr.rule_from_str("{HOLA,COMO} => {ESTA}")]
        expected_2 = [cr.rule_from_str("{COMO,HOLA} => {ESTA}")]
        self.assertEqual(expected_1, result)
        self.assertEqual(expected_2, result)

    def test_antecedents(self):
        result = cr.antecedents([
           cr.rule_from_str("{HOLA,TODO} => {BIEN}"),
           cr.rule_from_str("{TEST} => {ASDF}") 
        ])
        expected = [{"HOLA", "TODO"}, {"TEST"}]
        self.assertEqual(expected, result)

    def test_consequents(self):
        result = cr.consequents([
           cr.rule_from_str("{HOLA,TODO} => {BIEN}"),
           cr.rule_from_str("{TEST} => {ASDF}") 
        ])
        expected = [{"BIEN"}, {"ASDF"}]
        self.assertEqual(expected, result)

    def test_itemsets(self):
        result = cr.itemsets([
           cr.rule_from_str("{HOLA,TODO} => {BIEN}"),
           cr.rule_from_str("{TODO} => {BIEN}"),
           cr.rule_from_str("{TEST} => {ASDF}") 
        ])
        expected = {"HOLA", "TODO", "BIEN", "TEST", "ASDF"}
        self.assertEqual(expected, result)

    def test_sets_intersection_exact(self):
        result = cr.sets_intersection_exact(
            [{"HOLA", "TODO", "BIEN"}, {"HOLA", "TODO"}],
            [{"CHAU", "TODO", "BIEN"}, {"CHAU", "TODO"}]
        )
        self.assertEqual([], result)

        result = cr.sets_intersection_exact(
            [{"HOLA", "TODO", "BIEN"}, {"HOLA", "TODO"}],
            [{"CHAU", "TODO", "BIEN"}, {"HOLA", "TODO"}]
        )
        self.assertEqual([{"HOLA", "TODO"}], result)


    def test_itemsets_intersection_exact(self):
        result = cr.itemsets_intersection_exact(
            {"HOLA", "TODO", "BIEN", "BLAB"},
            {"TODO", "BIEN", "CHAU", "BAII", "ASDF"},
        )
        expected = {"TODO", "BIEN"}
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()

