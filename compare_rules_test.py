import unittest
import pathlib
import pandas as pd

import compare_rules as cr
import info_rules as ir


class TestRuleComparison(unittest.TestCase):

    def test_interseccion_base(self) -> None:
        self.assertEqual([1], cr.generic_list_intersection([1, 2, 3], [1, 4, 5]))
        self.assertEqual([], cr.generic_list_intersection([1, 2, 3], [4, 5, 6]))
        self.assertEqual([], cr.generic_list_intersection([1, 2, 3], []))
        self.assertEqual([], cr.generic_list_intersection([], [4, 5, 6]))
        self.assertEqual(["hola"], cr.generic_list_intersection(["hola", "como", "estas"], ["hola", "komo", "estaz"]))

    def test_fast_interseccion(self) -> None:
        self.assertEqual([1], cr.fast_list_intersection([1, 2, 3], [1, 4, 5]))
        self.assertEqual([], cr.fast_list_intersection([1, 2, 3], [4, 5, 6]))
        self.assertEqual([], cr.fast_list_intersection([1, 2, 3], []))
        self.assertEqual([], cr.fast_list_intersection([], [4, 5, 6]))
        self.assertEqual(["hola"], cr.fast_list_intersection(["hola", "como", "estas"], ["hola", "komo", "estaz"]))

    def test_rules_intersection(self) -> None:
        result = cr.rules_intersection_exact(
            [   ir.rule_from_str("{HOLA,COMO} => {ESTA}"),
                ir.rule_from_str("{ESTO,NOOO} => {ESTA}")],

            [   ir.rule_from_str("{COMO,HOLA} => {ESTA}")])

        # No importa el orden, la regla debe ser la misma en el build
        expected_1 = [ir.rule_from_str("{HOLA,COMO} => {ESTA}")]
        expected_2 = [ir.rule_from_str("{COMO,HOLA} => {ESTA}")]
        self.assertEqual(expected_1, result)
        self.assertEqual(expected_2, result)

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

    def test_mrs_txs_frecuencia_mayor_set(self) -> None:
        result = cr.mrs_txs_frecuencia_mayor_set(2, ["A", "A", "A", "B", "B", "C"])
        self.assertEqual({"A", "B"}, result)

    def test_mrs_txs_frecuencia_mayor_list(self) -> None:
        result = cr.mrs_txs_frecuencia_mayor_list(2, ["A", "A", "A", "B", "B", "C"])
        self.assertEqual(["A", "A", "A", "B", "B"], result)

    def test_mrs_frequency_map_from_mrs(self) -> None:
        mrs = ["A", "A", "B", "C", "B", "A"]
        result = cr.mrs_frequency_map_from_mrs(mrs)
        self.assertEqual({"A": 3, "B": 2, "C": 1}, result)


if __name__ == '__main__':
    unittest.main()
