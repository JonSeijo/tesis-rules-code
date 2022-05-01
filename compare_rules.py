import argparse
import nltk
import pathlib
import pandas as pd
from typing import Sized, Any, Iterable, List, Tuple, Set, TypeVar

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
    print("#items_unicos_a (mrs unicos en reglas):", len(set(itemset(rules_a))))
    print("#items_unicos_b (mrs unicos en reglas):", len(set(itemset(rules_b))))
    print()
    print("#consecuentes_unicos_a (en reglas):", len(set(consequents(rules_a))))
    print("#consecuentes_unicos_a (en reglas):", len(set(consequents(rules_b))))
    print()
    print("#antecedentes_unicos_a (en reglas):", len(set([frozenset(ant) for ant in antecedents(rules_a)])))
    print("#antecedentes_unicos_a (en reglas):", len(set([frozenset(ant) for ant in antecedents(rules_b)])))
    print()

def print_mrs_info(path_mr_a: str, path_mr_b: str) -> None:
    mrs_unicos_a = unique_mrs_from_path(path_mr_a)
    mrs_unicos_b = unique_mrs_from_path(path_mr_b)
    print("#mrs_unicos_a (en transacciones):", len(mrs_unicos_a))
    print("#mrs_unicos_b (en transacciones):", len(mrs_unicos_b))
    print()

def print_info(intersection: Sized, title) -> None:
    print("============================")
    print(title)
    print("#intersection:", len(intersection))
    print()

def unique_mrs_from_path(filepath: str) -> Set[str]:
    unique_mrs = set()
    with open(filepath) as mr_file:
        transactions = [tx.strip().replace(" ", "").split(",") for tx in mr_file.readlines()]
        return unique_mrs_from_transactions(transactions)
    return unique_mrs

def unique_mrs_from_transactions(txs: List[List[str]]) -> Set[str]:
    unique_mrs = set()
    for tx in txs:
        mrs = tx
        unique_mrs.update(mrs) # addAll
    return unique_mrs

def generic_list_intersection(
    collection_a: Iterable[Any], collection_b: Iterable[Any]
) -> List[Any]:
    return [ a for a in collection_a if a in collection_b ]

def generic_set_intersection(
    collection_a: Iterable[Any], collection_b: Iterable[Any]
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
) -> List[str]:
    return [ next(iter(rule[1])) for rule in rules ]

def itemset(
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
    return generic_list_intersection(consequents(rules_a), consequents(rules_b))

def mrs_interseccion_exacta() -> Set[str]:
    return itemsets_intersection_exact(itemset(rules_a), itemset(rules_b))

def levenshtein(s1: str, s2: str) -> int:
    return nltk.edit_distance(s1, s2)

def iterables_interseccion_lev_dist(dist: int, item_container_a: Iterable[str], item_container_b: Iterable[str]) -> Set[str]:
    interseccion = set()

    for item_a in set(item_container_a):
        for item_b in set(item_container_b):
            # item_a, item_b en la interseccion si existe b con distancia de edicion <= dist
            if levenshtein(item_a, item_b) <= dist:
                interseccion.add(item_a)
                interseccion.add(item_b)
                continue

    return interseccion


def mrs_interseccion_lev_1():
    return iterables_interseccion_lev_dist(1, itemset(rules_a), itemset(rules_b))

def mrs_interseccion_lev_2():
    return iterables_interseccion_lev_dist(2, itemset(rules_a), itemset(rules_b))

def consequents_intersection_lev_1():
    return iterables_interseccion_lev_dist(1, consequents(rules_a), consequents(rules_b))

# TODO: Pensar como sería una comparacion de antecedentes
def antecedents_interseccion_lev_dist(
    dist: int, 
    antecedents_a: List[Set[str]], 
    antecedents_b: List[Set[str]]
) -> List[Set[str]]:
    
    # Quiero ver si existe antecedent en A tq antecedent en B esta a dist <= 1
    for ant_a in antecedents_a:
        for ant_b in antecedents_b:
            pass
            # ant_a y ant_b son sets! de items
            # ¿que significa que dos SETS esten a distancia <= 1?

    return []

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run rules comparison')

    # parser.add_argument('path_rules_a',
    #     type=pathlib.Path,
    #     action='store',
    #     help='relative path to rules_a')

    # parser.add_argument('path_rules_b',
    #     type=pathlib.Path,
    #     action='store',
    #     help='relative path to rules_b')

    # args: argparse.Namespace = parser.parse_args()
    # path_rules_a = str(args.path_rules_a)
    # path_rules_b = str(args.path_rules_b)

    """
    output/rules/NEWAnk_len4_ALL_sub_s0.025_c0.9.csv
    output/rules/TPR1_len4_ALL_sub_s0.015_c0.75.csv
    """

    # TODO: Parametrizar family, support y confidence
    family_a = "NEWAnk_len4_ALL_sub"
    path_mr_a = f"output/clean_transactions/{family_a}.csv"
    path_rules_a = f"output/rules/{family_a}_s0.025_c0.9.csv"
    
    family_b = "TPR1_len4_ALL_sub"
    path_mr_b = f"output/clean_transactions/{family_b}.csv"
    path_rules_b = f"output/rules/{family_b}_s0.015_c0.75.csv"

    df_a = pd.read_csv(path_rules_a)
    df_b = pd.read_csv(path_rules_b)

    rules_a = build_rule_list_from_df(df_a)
    rules_b = build_rule_list_from_df(df_b)

    print_header()
    # print_mrs_info(path_mr_a, path_mr_b)
    print_info(interseccion_exacta(), "Interseccion exacta")
    print_info(interseccion_exacta_antecedentes(), "Interseccion exacta antecedentes")
    print_info(interseccion_exacta_consecuentes(), "Interseccion exacta consecuentes")
    print_info(mrs_interseccion_exacta(), "Interseccion exacta MRs (itemsets unicos)")
    print_info(mrs_interseccion_lev_1(), "Interseccion distancia=1 MRs (itemsets unicos)")
    print_info(mrs_interseccion_lev_2(), "Interseccion distancia=2 MRs (itemsets unicos)")
    print_info(consequents_intersection_lev_1(), "Interseccion distancia=1 Consecuentes (itemsets unicos)")

