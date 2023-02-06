# python3 -m unittest info_rules_test.py

import unittest

import info_rules as ir

class TestInfoRules(unittest.TestCase):

    def test_build_itemset(self) -> None:
        result = ir.build_itemset("{GNTA,HLAA,NTAL,PLHL}")
        expected = set(["GNTA", "HLAA", "NTAL", "PLHL"])
        self.assertEqual(expected, result)

        with self.assertRaises(ir.RuleBuildException):
            ir.build_itemset("GNTA,HLAA,NTAL,PLHL")


    def test_rule_from_str(self) -> None:
        # "{ALHV,LHIA} => {LHVA}"  ----> ({ALHV,LHIA}, {LHVA})
        result = ir.rule_from_str("{ALHV,LHIA} => {LHVA}")
        expected = (set(["ALHV", "LHIA"]), set(["LHVA"]))
        self.assertEqual(expected, result)

        with self.assertRaises(ir.RuleBuildException):
            ir.rule_from_str("{ALHV,LHIA},{LHVA}")

        with self.assertRaises(ir.RuleBuildException):
            ir.rule_from_str("{ALHV,LHIA} => ")


    def test_all_mrs_from_transactions(self) -> None:
        result = ir.all_mrs_from_transactions([["AAAA"], ["AAAB", "AAAC"]])
        self.assertEqual(["AAAA", "AAAB", "AAAC"], result)


    def test_itemsets(self) -> None:
        result = ir.itemset([
           ir.rule_from_str("{HOLA,TODO} => {BIEN}"),
           ir.rule_from_str("{TODO} => {BIEN}"),
           ir.rule_from_str("{TEST} => {ASDF}") 
        ])
        expected = {"HOLA", "TODO", "BIEN", "TEST", "ASDF"}
        self.assertEqual(expected, result)

    def test_antecedents(self) -> None:
        result = ir.antecedents([
           ir.rule_from_str("{HOLA,TODO} => {BIEN}"),
           ir.rule_from_str("{TEST} => {ASDF}") 
        ])
        expected = [{"HOLA", "TODO"}, {"TEST"}]
        self.assertEqual(expected, result)

    def test_consequents(self) -> None:
        result = ir.consequents([
           ir.rule_from_str("{HOLA,TODO} => {BIEN}"),
           ir.rule_from_str("{TEST} => {ASDF}") 
        ])
        # expected = [{"BIEN"}, {"ASDF"}]  old version
        expected = ["BIEN", "ASDF"]
        self.assertEqual(expected, result)


    def test_build_metadata(self) -> None:
        metadata = ir.build_rule_metadata_from_rule_filename(
            "output/rules/TPR1_len4_ALL_sub_s0.025_c0.9.csv"
        )

        self.assertEqual("TPR1_len4_ALL_sub_s0.025_c0.9", metadata.rules_filename)
        self.assertEqual("TPR1", metadata.family)
        self.assertEqual("len4", metadata.min_len)
        self.assertEqual("mrs", metadata.transaction_type)
        self.assertEqual("ALL", metadata.maximal_repeat_type)
        self.assertEqual("sub", metadata.clean_mode)
        self.assertEqual("0.025", metadata.min_support)
        self.assertEqual("0.9", metadata.min_confidence)


    def test_build_metadata_nomrs(self) -> None:
        metadata = ir.build_rule_metadata_from_rule_filename(
            "output/rules/TPR1_len4_nomrs_s0.025_c0.9.csv"
        )

        self.assertEqual("TPR1_len4_nomrs_s0.025_c0.9", metadata.rules_filename)
        self.assertEqual("TPR1", metadata.family)
        self.assertEqual("len4", metadata.min_len)
        self.assertEqual("nomrs", metadata.transaction_type)
        self.assertEqual(None, metadata.maximal_repeat_type)
        self.assertEqual(None, metadata.clean_mode)
        self.assertEqual("0.025", metadata.min_support)
        self.assertEqual("0.9", metadata.min_confidence)


    def test_build_metadata_long_familyname(self) -> None:
        metadata = ir.build_rule_metadata_from_rule_filename(
            "output/rules/NEWAnk_TEST_len4_ALL_min_s0.4_c0.9.csv"
        )

        self.assertEqual("NEWAnk_TEST_len4_ALL_min_s0.4_c0.9", metadata.rules_filename)
        self.assertEqual("NEWAnk_TEST", metadata.family)
        self.assertEqual("len4", metadata.min_len)
        self.assertEqual("mrs", metadata.transaction_type)
        self.assertEqual("ALL", metadata.maximal_repeat_type)
        self.assertEqual("min", metadata.clean_mode)
        self.assertEqual("0.4", metadata.min_support)
        self.assertEqual("0.9", metadata.min_confidence)


    def test_build_metadata_long_familyname_v2(self) -> None:
        metadata = ir.build_rule_metadata_from_rule_filename(
            "output/rules/NEWAnk_SCRAMBLED_TEST_v2_len4_ALL_min_s0.4_c0.9.csv"
        )

        self.assertEqual("NEWAnk_SCRAMBLED_TEST_v2", metadata.family)
        self.assertEqual("len4", metadata.min_len)
        self.assertEqual("mrs", metadata.transaction_type)
        self.assertEqual("ALL", metadata.maximal_repeat_type)
        self.assertEqual("min", metadata.clean_mode)
        self.assertEqual("0.4", metadata.min_support)
        self.assertEqual("0.9", metadata.min_confidence)



if __name__ == '__main__':
    unittest.main()
