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







if __name__ == '__main__':
    unittest.main()
