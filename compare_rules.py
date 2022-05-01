import argparse
import pathlib
import pandas as pd
from typing import List, Tuple, Set

class RuleBuildException(Exception):
    pass

# s = {GNTA,HLAA,NTAL,PLHL,TPLH}
def build_itemset(s: str) -> Set[str]:
    if len(s) <= 2 or s[0] != "{" or s[-1] != "}":
        raise RuleBuildException()

    s = s[1:-1]
    ls = s.split(",")
    return set(ls)


# "{ALHV,LHIA} => {LHVA}"  ----> ({ALHV,LHIA}, {LHVA})
def rule_from_str(rule_str: str) -> Tuple[Set[str], Set[str]]:
    if " => " not in rule_str:
        raise RuleBuildException()
    
    splitted = rule_str.split(" => ")

    if len(splitted) != 2:
        raise RuleBuildException()

    left, right = splitted

    if len(left) == 0 or len(right) == 0:
        raise RuleBuildException()

    return build_itemset(left), build_itemset(right)


def build_rule_list_from_df(df_rules):
    return [rule_from_str(rule[0]) for idx, rule in df_rules[["rules"]].iterrows()]


def print_header():
    print("============================")
    print("rules_a:", path_rules_a.split("/")[-1])
    print("rules_b:", path_rules_b.split("/")[-1])
    print()
    print("#rules_a:", len(rules_a))
    print("#rules_b:", len(rules_b))
    print()

def print_info(intersection, title):
    print("============================")
    print(title)
    print("#intersection:", len(intersection))
    print()

def list_intersection(list_a, list_b):
    return [ item for item in list_b if item in list_a ]

def rules_intersection_exact(
    rules_a: List[Tuple[Set[str], Set[str]]], 
    rules_b: List[Tuple[Set[str], Set[str]]]
) -> List[Tuple[Set[str], Set[str]]]:
    return [ rule for rule in rules_a if rule in rules_b ]

def sets_intersection_exact(
    set_a: List[Set[str]],
    set_b: List[Set[str]],
) -> List[Set[str]]:
    return [ itemset for itemset in set_a if itemset in set_b ]

def antecedents(
    rules: List[Tuple[Set[str], Set[str]]]
) -> List[Set[str]]:
    return [ rule[0] for rule in rules ]

def consequents(
    rules: List[Tuple[Set[str], Set[str]]]
) -> List[Set[str]]:
    return [ rule[1] for rule in rules ]

def _itemsets(rule_list):
    all_itemsets = set()
    for rule in rule_list:
        print()


def interseccion_exacta():
    return rules_intersection_exact(rules_a, rules_b)

def interseccion_exacta_antecedentes():
    return sets_intersection_exact(antecedents(rules_a), antecedents(rules_b))

def interseccion_exacta_consecuentes():
    return sets_intersection_exact(consequents(rules_a), consequents(rules_b))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run rules comparison')

    parser.add_argument('path_rules_a',
        type=pathlib.Path,
        action='store',
        help='relative path to rules_a')

    parser.add_argument('path_rules_b',
        type=pathlib.Path,
        action='store',
        help='relative path to rules_b')

    # rules_a = "ank_len4_ALL_s0.025_c0.9.csv"
    # rules_b = "NEWAnk_len4_ALL_s0.025_c0.9.csv"

    args = parser.parse_args()
    path_rules_a = str(args.path_rules_a)
    path_rules_b = str(args.path_rules_b)

    df_a = pd.read_csv(path_rules_a)
    df_b = pd.read_csv(path_rules_b)

    rules_a = build_rule_list_from_df(df_a)
    rules_b = build_rule_list_from_df(df_b)

    print_header()
    print_info(interseccion_exacta(), "Interseccion exacta")
    print_info(interseccion_exacta_antecedentes(), "Interseccion exacta antecedentes")
    print_info(interseccion_exacta_consecuentes(), "Interseccion exacta consecuentes")

