import argparse
import nltk
import pathlib
import pandas as pd
from typing import Sized, Any, List, Tuple, Set, TypeVar


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


def build_rule_list_from_df(df_rules) -> List[Tuple[Set[str], Set[str]]]:
    return [rule_from_str(rule[0]) for idx, rule in df_rules[["rules"]].iterrows()]


def print_header() -> None:
    print("============================")
    print("rules_a:", path_rules_a.split("/")[-1])
    print("rules_b:", path_rules_b.split("/")[-1])
    print()
    print("#rules_a:", len(rules_a))
    print("#rules_b:", len(rules_b))
    print()
    print("#itemsets_a (unicos):", len(itemsets(rules_a)))
    print("#itemsets_b (unicos):", len(itemsets(rules_b)))
    print()

def print_info(intersection: Sized, title) -> None:
    print("============================")
    print(title)
    print("#intersection:", len(intersection))
    print()


def generic_list_intersection(
    collection_a: List[Any], collection_b: List[Any]
) -> List[Any]:
    return [ a for a in collection_a if a in collection_b ]

def generic_set_intersection(
    collection_a: Set[Any], collection_b: Set[Any]
) -> Set[Any]:
    return { a for a in collection_a if a in collection_b }


def list_intersection(list_a, list_b):
    return generic_list_intersection(list_a, list_b)

def rules_intersection_exact(
    rules_a: List[Tuple[Set[str], Set[str]]], 
    rules_b: List[Tuple[Set[str], Set[str]]]
) -> List[Tuple[Set[str], Set[str]]]:
    # Esto asume comparador de rules!
    return generic_list_intersection(rules_a, rules_b)

def sets_intersection_exact(
    set_a: List[Set[str]],
    set_b: List[Set[str]],
) -> List[Set[str]]:
    return generic_list_intersection(set_a, set_b)

def itemsets_intersection_exact(
    itemsets_a: Set[str],
    itemsets_b: Set[str],
) -> Set[str]:
    return generic_set_intersection(itemsets_a, itemsets_b)

def antecedents(
    rules: List[Tuple[Set[str], Set[str]]]
) -> List[Set[str]]:
    return [ rule[0] for rule in rules ]

def consequents(
    rules: List[Tuple[Set[str], Set[str]]]
) -> List[Set[str]]:
    return [ rule[1] for rule in rules ]

def itemsets(
    rules: List[Tuple[Set[str], Set[str]]]
) -> Set[str]:
    all_itemsets = set()
    for rule in rules:
        for itemset in rule[0]:  # Antecedent
            all_itemsets.add(itemset)
        for itemset in rule[1]:  # Consequent
            all_itemsets.add(itemset)
    return all_itemsets

def interseccion_exacta() -> List[Tuple[Set[str], Set[str]]]:
    return rules_intersection_exact(rules_a, rules_b)

def interseccion_exacta_antecedentes() -> List[Set[str]]:
    return sets_intersection_exact(antecedents(rules_a), antecedents(rules_b))

def interseccion_exacta_consecuentes() -> List[Set[str]]:
    return sets_intersection_exact(consequents(rules_a), consequents(rules_b))

def mrs_interseccion_exacta() -> Set[str]:
    return itemsets_intersection_exact(itemsets(rules_a), itemsets(rules_b))

def levenshtein(s1: str, s2: str) -> int:
    return nltk.edit_distance(s1, s2)

def mrs_interseccion_lev_1():
    itemsets_a = itemsets(rules_a)
    itemsets_b = itemsets(rules_b)
    interseccion = set()

    for item_a in itemsets_a:
        for item_b in itemsets_b:
            # item_a en la interseccion si existe b con distancia de edicion <= 1
            if levenshtein(item_a, item_b) <= 1:
                interseccion.add(item_a)

    return interseccion

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

    args: argparse.Namespace = parser.parse_args()
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
    print_info(mrs_interseccion_exacta(), "Interseccion exacta MRs (itemsets unicos)")
    print_info(mrs_interseccion_lev_1(), "Interseccion distancia=1 MRs (itemsets unicos)")

