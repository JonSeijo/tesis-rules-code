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

def print_mrs_info() -> None:
    print("#mrs_txs_a (en transacciones):", len(mrs_txs_a))
    print("#mrs_txs_b (en transacciones):", len(mrs_txs_b))
    print()
    print("#mrs_unicos_a (en transacciones):", len(mrs_unicos_a))
    print("#mrs_unicos_b (en transacciones):", len(mrs_unicos_b))
    print()

def print_info(intersection: Sized, title) -> None:
    print("============================")
    print(title)
    print("#intersection:", len(intersection))
    print()

def all_mrs_from_path(filepath: str) -> List[str]:
    with open(filepath) as mr_file:
        transactions = [tx.strip().replace(" ", "").split(",") for tx in mr_file.readlines()]
        return all_mrs_from_transactions(transactions)
    raise Exception("Error reading transactions from", filepath)

def unique_mrs_from_path(filepath: str) -> Set[str]:
    unique_mrs = set()
    with open(filepath) as mr_file:
        transactions = [tx.strip().replace(" ", "").split(",") for tx in mr_file.readlines()]
        return unique_mrs_from_transactions(transactions)
    return unique_mrs

def all_mrs_from_transactions(txs: List[List[str]]) -> List[str]:
    return [mr for tx in txs for mr in tx]

def unique_mrs_from_transactions(txs: List[List[str]]) -> Set[str]:
    unique_mrs = set()
    for tx in txs:
        mrs = tx
        unique_mrs.update(mrs) # addAll
    return unique_mrs

# Requires hashable elements!
def fast_list_intersection(
    collection_a: Iterable[Any], collection_b: Iterable[Any]
) -> List[Any]:
    hash_collection_b = set(collection_b)
    return [ a for a in collection_a if a in hash_collection_b ]

def generic_list_intersection(
    collection_a: Iterable[Any], collection_b: Iterable[Any]
) -> List[Any]:
    return [ a for a in collection_a if a in collection_b ]

def generic_set_intersection(
    collection_a: Iterable[Any], collection_b: Iterable[Any]
) -> Set[Any]:
    return { a for a in collection_a if a in collection_b }

def rules_intersection_exact(
    rules_a: List[Tuple[Set[str], Set[str]]], 
    rules_b: List[Tuple[Set[str], Set[str]]]
) -> List[Tuple[Set[str], Set[str]]]:
    # Esto asume comparador de rules!
    return generic_list_intersection(rules_a, rules_b)

def sets_intersection_exact(set_a: List[Set[str]], set_b: List[Set[str]]) -> List[Set[str]]:
    return generic_list_intersection(set_a, set_b)

def itemsets_intersection_exact(itemsets_a: Set[str], itemsets_b: Set[str]) -> Set[str]:
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

def mrs_reglas_interseccion_exacta() -> Set[str]:
    return itemsets_intersection_exact(itemset(rules_a), itemset(rules_b))

def levenshtein(s1: str, s2: str) -> int:
    return nltk.edit_distance(s1, s2)

def iterables_interseccion_lev_dist(dist: int, item_container_a: Iterable[str], item_container_b: Iterable[str]) -> Set[str]:
    interseccion = set()

    list_container_a = list(set(item_container_a)) # Paso a set para asegurarme que no haya repetidos
    list_container_b = list(set(item_container_b))

    for item_a in list_container_a:
        for item_b in list_container_b:
            # item_a, item_b en la interseccion si existe b con distancia de edicion <= dist
            if levenshtein(item_a, item_b) <= dist:
                interseccion.add(item_a)
                interseccion.add(item_b)

    return interseccion


def mrs_reglas_interseccion_lev_1() -> Set[str]:
    return iterables_interseccion_lev_dist(1, itemset(rules_a), itemset(rules_b))

def mrs_reglas_interseccion_lev_2() -> Set[str]:
    return iterables_interseccion_lev_dist(2, itemset(rules_a), itemset(rules_b))

def mrs_txs_interseccion_exacta() -> Set[str]:
    return itemsets_intersection_exact(mrs_unicos_a, mrs_unicos_b)

def mrs_txs_interseccion_lev_1(mrs_a: Set[str], mrs_b: Set[str]) -> Set[str]:
    intersection = set()
    for mr in mrs_a:
        for mr_dist1 in words_with_dist_1(mr):
            if mr_dist1 in mrs_b:
                intersection.add(mr)
                intersection.add(mr_dist1)

    return intersection

def words_with_dist_1(word: str):
    words_dist_1 = set()
    words_dist_1.add(word)
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            newword = word[:i] + c.upper() + word[i+1:]
            words_dist_1.add(newword)
    return words_dist_1

# Las de frecuencia mayor sin repetidos
def mrs_txs_frecuencia_mayor_set(freq: int, mrs: List[str]) -> Set[str]:
    return set(mrs_txs_frecuencia_mayor_list(freq, mrs))

# Esta version incluse TODAS las apariciones de freq mayor
def mrs_txs_frecuencia_mayor_list(freq: int, mrs: List[str]) -> List[str]:
    counts = dict()
    for mr in mrs:
        counts[mr] = counts.get(mr, 0) + 1
    
    frecuentes = []
    for mr, count in counts.items():
        if count >= freq:
            # Agrego uno por cada aparicion
            for _ in range(count):
                frecuentes.append(mr)
    return frecuentes



def mrs_txs_interseccion_lev_1_frecuentes(
    frecuencia_minima: int, mrs_txs_a: List[str], mrs_txs_b: List[str]) -> Set[str]:
    # El problema es que son DEMASIADAS mrs. Tomo las mas frecuentes antes de tomar la interseccion a distancia=1.
    #   Demasiadas commbinaciones posibles sino. 
    freq_a = mrs_txs_frecuencia_mayor_set(frecuencia_minima, mrs_txs_a) # TODO: Si lo cambio por unicos, pyre deberia avisarme que algo esta mal...
    freq_b = mrs_txs_frecuencia_mayor_set(frecuencia_minima, mrs_txs_b)

    # print("  ==================================")
    # print(f" -- Frecuencia minima: {frecuencia_minima} - freq_a cant:", len(freq_a))
    # print(f" -- Frecuencia minima: {frecuencia_minima} - freq_b cant:", len(freq_b))

    return mrs_txs_interseccion_lev_1(1, freq_a, freq_b)

def consequents_intersection_lev_1() -> Set[str]:
    return iterables_interseccion_lev_dist(
        1, consequents(rules_a), consequents(rules_b))


# TODO: Pensar como sería una comparacion de antecedentes??
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

    mrs_txs_a = all_mrs_from_path(path_mr_a)
    mrs_txs_b = all_mrs_from_path(path_mr_b)

    mrs_unicos_a = set(mrs_txs_a)
    mrs_unicos_b = set(mrs_txs_b)

    print_header()
    print_mrs_info()
    print_info(interseccion_exacta(), "Interseccion exacta")
    print_info(interseccion_exacta_antecedentes(), "Interseccion exacta antecedentes")
    print_info(interseccion_exacta_consecuentes(), "Interseccion exacta consecuentes")
    print_info(mrs_reglas_interseccion_exacta(), "Interseccion exacta MRs [en reglas] (itemsets unicos)")
    print_info(mrs_reglas_interseccion_lev_1(), "Interseccion distancia=1 MRs [en reglas] (itemsets unicos)")
    print_info(mrs_reglas_interseccion_lev_2(), "Interseccion distancia=2 MRs [en reglas] (itemsets unicos)")
    print_info(consequents_intersection_lev_1(), "Interseccion distancia=1 Consecuentes (itemsets unicos)")
    print_info(mrs_txs_interseccion_exacta(), "Interseccion exacta MRs [en TXs]")
    print_info(mrs_txs_interseccion_lev_1_frecuentes(1000, mrs_txs_a, mrs_txs_b), "Interseccion en frecuentes. distancia=1 MRs [en TXs]")
    print_info(mrs_txs_interseccion_lev_1(mrs_unicos_a, mrs_unicos_b), "Interseccion distancia=1 MRs [en TXs]")
