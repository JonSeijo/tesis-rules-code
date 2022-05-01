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



if __name__ == '__main__':
    unittest.main()


# def rule_list(df_rules):
#   return [from_str(rule[0]) for idx, rule in df_rules[["rules"]].iterrows()]


# def print_header():
#   print("============================")
#   print("rules_a:", path_rules_a.split("/")[-1])
#   print("rules_b:", path_rules_b.split("/")[-1])
#   print()
#   print("#rules_a:", len(rules_a))
#   print("#rules_b:", len(rules_b))
#   print()

# def print_info(intersection, title):
#   print("============================")
#   print(title)
#   print("#intersection:", len(intersection))
#   print()

# def _interseccion(list_a, list_b):
#   return [ item for item in list_b if item in list_a ]

# def _antecedentes(rule_list):
#   return [ rule[0] for rule in rule_list ]

# def _consecuentes(rule_list):
#   return [ rule[1] for rule in rule_list ]

# def _itemsets_from_rule(rule):
#   return rule_str.split(",")

# def _itemsets(rule_list):
#   all_itemsets = set()
#   for rule in rule_list:
#       print(rule)


# def interseccion_exacta():
#   return _interseccion(rules_a, rules_b)

# def interseccion_exacta_antecedentes():
#   return _interseccion(_antecedentes(rules_a), _antecedentes(rules_b))

# def interseccion_exacta_consecuentes():
#   return _interseccion(_consecuentes(rules_a), _consecuentes(rules_b))


# if __name__ == '__main__':
#   parser = argparse.ArgumentParser(description='Run rules comparison')

#   parser.add_argument('path_rules_a',
#       type=pathlib.Path,
#       action='store',
#       help='relative path to rules_a')

#   parser.add_argument('path_rules_b',
#       type=pathlib.Path,
#       action='store',
#       help='relative path to rules_b')

#   # rules_a = "ank_len4_ALL_s0.025_c0.9.csv"
#   # rules_b = "NEWAnk_len4_ALL_s0.025_c0.9.csv"

#   args = parser.parse_args()
#   path_rules_a = str(args.path_rules_a)
#   path_rules_b = str(args.path_rules_b)

#   df_a = pd.read_csv(path_rules_a)
#   df_b = pd.read_csv(path_rules_b)

#   rules_a = rule_list(df_a)
#   rules_b = rule_list(df_b)

#   print_header()
#   print_info(interseccion_exacta(), "Interseccion exacta")
#   print_info(interseccion_exacta_antecedentes(), "Interseccion exacta antecedentes")
#   print_info(interseccion_exacta_consecuentes(), "Interseccion exacta consecuentes")

# # for l,r in rules_in_a_not_in_b:
# #     print(f"{l} -> {r}")


# # Pequeña exploracion:
# # for l, r in rules_a:
# #     mayor_4 = False
# #     for x in l:
# #         if len(x) >  4:
# #             mayor_4 = True
# #     for x in r:
# #         if len(x) > 4:
# #             mayor_4 = True

# #     if mayor_4:
# #         print(f"{l} -> {r}")
