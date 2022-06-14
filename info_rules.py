import pandas as pd
from typing import Sized, Any, Dict, Iterable, List, Tuple, Set, TypeVar


def antecedents(
    rules: List[Tuple[Set[str], Set[str]]]
) -> List[Set[str]]:
    return [ frozenset(rule[0]) for rule in rules ]

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

def transactions_from_path(filepath: str) -> List[List[str]]:
    with open(filepath) as txs_file:
        transactions = [tx.strip().replace(" ", "").split(",") for tx in txs_file.readlines()]
    return transactions

def all_mrs_from_path(txs_filepath: str) -> List[str]:
    transactions = transactions_from_path(txs_filepath)
    return all_mrs_from_transactions(transactions)

# TODO: Renombrar, no necesariamente son mrs (ojo Jupyters)
def all_mrs_from_transactions(txs: List[List[str]]) -> List[str]:
    return [mr for tx in txs for mr in tx]


def build_rule_list_from_df(df_rules) -> List[Tuple[Set[str], Set[str]]]:
    return [rule_from_str(rule[0]) for idx, rule in df_rules[["rules"]].iterrows()]

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

# s = {GNTA,HLAA,NTAL,PLHL,TPLH}
def build_itemset(s: str) -> Set[str]:
    if len(s) <= 2 or s[0] != "{" or s[-1] != "}":
        raise RuleBuildException()

    s = s[1:-1]
    ls = s.split(",")
    return set(ls)

class RuleBuildException(Exception):
    pass

def build_info_rules_for(family, min_len, mr_type, min_support, min_confidence):
    print(f"build_info_rules_for({family}, {min_len}, {mr_type}, {min_support}, {min_confidence})")

    info_rules = {}

    info_rules["family"] = family
    info_rules["min_len"] = min_len
    info_rules["mr_type"] = mr_type
    info_rules["min_support"] = min_support
    info_rules["min_confidence"] = min_confidence

    info_rules["path_transactions"] = f"output/clean_transactions/{family}_{min_len}_{mr_type}.csv"
    info_rules["path_rules"] = f"output/rules/{family}_{min_len}_{mr_type}_s{min_support}_c{min_confidence}.csv"

    df_rules = pd.read_csv(info_rules["path_rules"])
    rules = build_rule_list_from_df(df_rules)

    info_rules["rules_amount"] = len(rules)
    info_rules["rules_unique_items"] = len(set(itemset(rules)))
    info_rules["rules_unique_antecedents"] = len(set(antecedents(rules)))
    info_rules["rules_unique_consecuents"] = len(set(consequents(rules)))

    transactions = transactions_from_path(info_rules["path_transactions"])
    txs_items = all_mrs_from_transactions(transactions)

    info_rules["txs_amount"] = len(transactions)
    info_rules["txs_items"] = len(txs_items)
    info_rules["txs_unique_items"] = len(set(txs_items))

    return info_rules


if __name__ == '__main__':

    family = "NEWAnk"
    min_len = "len4"
    mr_type = "ALL_sub"
    min_support = "0.025"
    min_confidence = "0.9"

    info_rules = build_info_rules_for(family, min_len, mr_type, min_support, min_confidence)

    for k, v in info_rules.items():
        print(f"{k}: {v}")
