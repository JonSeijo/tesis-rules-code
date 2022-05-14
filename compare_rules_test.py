import unittest
import pathlib
import pandas as pd

import compare_rules as cr

class TestRuleComparison(unittest.TestCase):

    def test_build_itemset(self) -> None:
        result = cr.build_itemset("{GNTA,HLAA,NTAL,PLHL}")
        expected = set(["GNTA", "HLAA", "NTAL", "PLHL"])
        self.assertEqual(expected, result)

        with self.assertRaises(cr.RuleBuildException):
            cr.build_itemset("GNTA,HLAA,NTAL,PLHL")


    def test_rule_from_str(self) -> None:
        # "{ALHV,LHIA} => {LHVA}"  ----> ({ALHV,LHIA}, {LHVA})
        result = cr.rule_from_str("{ALHV,LHIA} => {LHVA}")
        expected = (set(["ALHV", "LHIA"]), set(["LHVA"]))
        self.assertEqual(expected, result)

        with self.assertRaises(cr.RuleBuildException):
            cr.rule_from_str("{ALHV,LHIA},{LHVA}")

        with self.assertRaises(cr.RuleBuildException):
            cr.rule_from_str("{ALHV,LHIA} => ")

    def test_interseccion_base(self) -> None:
        self.assertEqual([1], cr.list_intersection([1, 2, 3], [1, 4, 5]))
        self.assertEqual([], cr.list_intersection([1, 2, 3], [4, 5, 6]))
        self.assertEqual([], cr.list_intersection([1, 2, 3], []))
        self.assertEqual([], cr.list_intersection([], [4, 5, 6]))
        self.assertEqual(["hola"], cr.list_intersection(["hola", "como", "estas"], ["hola", "komo", "estaz"]))

    def test_rules_intersection(self) -> None:
        result = cr.rules_intersection_exact(
            [   cr.rule_from_str("{HOLA,COMO} => {ESTA}"),
                cr.rule_from_str("{ESTO,NOOO} => {ESTA}")],

            [   cr.rule_from_str("{COMO,HOLA} => {ESTA}")])

        # No importa el orden, la regla debe ser la misma en el build
        expected_1 = [cr.rule_from_str("{HOLA,COMO} => {ESTA}")]
        expected_2 = [cr.rule_from_str("{COMO,HOLA} => {ESTA}")]
        self.assertEqual(expected_1, result)
        self.assertEqual(expected_2, result)

    def test_antecedents(self) -> None:
        result = cr.antecedents([
           cr.rule_from_str("{HOLA,TODO} => {BIEN}"),
           cr.rule_from_str("{TEST} => {ASDF}") 
        ])
        expected = [{"HOLA", "TODO"}, {"TEST"}]
        self.assertEqual(expected, result)

    def test_consequents(self) -> None:
        result = cr.consequents([
           cr.rule_from_str("{HOLA,TODO} => {BIEN}"),
           cr.rule_from_str("{TEST} => {ASDF}") 
        ])
        # expected = [{"BIEN"}, {"ASDF"}]  old version
        expected = ["BIEN", "ASDF"]
        self.assertEqual(expected, result)

    def test_itemsets(self) -> None:
        result = cr.itemset([
           cr.rule_from_str("{HOLA,TODO} => {BIEN}"),
           cr.rule_from_str("{TODO} => {BIEN}"),
           cr.rule_from_str("{TEST} => {ASDF}") 
        ])
        expected = {"HOLA", "TODO", "BIEN", "TEST", "ASDF"}
        self.assertEqual(expected, result)

    def test_sets_intersection_exact(self) -> None:
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


    def test_itemsets_intersection_exact(self) -> None:
        result = cr.itemsets_intersection_exact(
            {"HOLA", "TODO", "BIEN", "BLAB"},
            {"TODO", "BIEN", "CHAU", "BAII", "ASDF"},
        )
        expected = {"TODO", "BIEN"}
        self.assertEqual(expected, result)

    def test_levenshtein(self) -> None:
        self.assertEqual(1, cr.levenshtein("CASA", "TASA"))
        self.assertEqual(2, cr.levenshtein("CAZA", "TASA"))
        self.assertEqual(4, cr.levenshtein("", "TASA"))
        self.assertEqual(0, cr.levenshtein("ASDF", "ASDF"))

    def test_iterables_intersection_lev_dist(self) -> None:
        # Tanto "casa" como "tasa" estan a distancia 1, ambos estan en la interseccion
        result = cr.iterables_interseccion_lev_dist(1, {"CASA"}, {"TASA"})
        self.assertEqual({"CASA", "TASA"}, result)

        result = cr.iterables_interseccion_lev_dist(1, {"CASA"}, {"CASA"})
        self.assertEqual({"CASA"}, result)

        result = cr.iterables_interseccion_lev_dist(1, {"CASA"}, {"PALA"})
        self.assertEqual(set(), result)

        result = cr.iterables_interseccion_lev_dist(2, {"CASA", "ASDF"}, {"TAPA", "ASER"})
        self.assertEqual({"CASA", "ASDF", "TAPA", "ASER"}, result)

    def test_words_with_dist_1(self) -> None:
        result = cr.words_with_dist_1("AAAA")
        for item in ["AAAA", "BAAA", "ABAA", "AABA", "AAAB", "AZAA", "PAAA"]:
            self.assertTrue(item in result)

        self.assertTrue("AABB" not in result)
        self.assertTrue("AA" not in result)
        self.assertTrue("BBBB" not in result)

    def test_mrs_txs_intersection_lev_1(self) -> None:
        # Tanto "casa" como "tasa" estan a distancia 1, ambos estan en la interseccion
        result = cr.mrs_txs_interseccion_lev_1({"CASA"}, {"TASA"})
        self.assertEqual({"CASA", "TASA"}, result)

        result = cr.mrs_txs_interseccion_lev_1({"CASA"}, {"CASA"})
        self.assertEqual({"CASA"}, result)

        result = cr.mrs_txs_interseccion_lev_1({"CASA"}, {"PALA"})
        self.assertEqual(set(), result)

        result = cr.mrs_txs_interseccion_lev_1({"AAAA", "AAAB"}, {"BAAA", "BAAB"})
        self.assertEqual({"AAAA", "AAAB", "BAAA", "BAAB"}, result)


if __name__ == '__main__':
    unittest.main()
