import ntpath
import re

from dataclasses import dataclass
import pandas as pd
from typing import Sized, Any, Dict, Iterable, List, Tuple, Set, TypeVar

# TODO: Use pre-exisiting classes for rules

# import importlib
# rg = importlib.import_module("main_code.rulegroup.rulegroup")
import main_code.rulegroup.rulegroup as rg


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
    if df_rules.empty:
        return []
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

def get_ruletypes(rules: List[rg.Rule]) -> List[str]:
    ruletypes = []
    for rule in rules:
        rtype = rule.getRuleTypeText()
        ruletypes.append(rtype)
    return ruletypes

def ruletypes_with(substr: str, rules: List[str], ruletypes: List[str]) -> List[str]:
    matching = []
    for rule, rtype in zip(rules, ruletypes):
        if substr in rtype:
            matching.append((rule, rtype))
    return matching

def simplify_ruletype(ruletype: str) -> str:
    if "Agrega" in ruletype:
        return "Agrega"
    return ruletype

def build_df_rules_from_path(path: str) -> pd.DataFrame:
    print("Loading rules file from:", path)
    df_rules = pd.read_csv(path)

    rules = [ rg.Rule(rule_str) for rule_str in list(df_rules["rules"])]


    # print(df_rules.columns)
    # Already in index: ['rules', 'support', 'confidence', 'coverage', 'lift', 'count']

    df_rules["antecedent"] = [ ','.join(sorted(rule.antecedent)) for rule in rules ]
    df_rules["consequent"] = [ rule.consequent for rule in rules ]

    df_rules["rule_size"] = [ 1 + len(rule.antecedent) for rule in rules ]

    print("Classifying rules...")
    ruletypes = get_ruletypes(rules)
    ruletypes_simple = list(map(simplify_ruletype, ruletypes))

    df_rules["ruletype"] = ruletypes
    df_rules["ruletype_simple"] = ruletypes_simple

    return df_rules


@dataclass
class RuleMetadata:
    rules_filename: str
    family: str
    min_len: str
    transaction_type: str
    maximal_repeat_type: str
    clean_mode: str
    min_support: str
    min_confidence: str
    

def build_rule_metadata_from_rule_filename(rules_filename_path):
    s_metadata = ntpath.basename(rules_filename_path) # Me quedo con el nombre del archivo (lo de despues de ../../ )
    s_metadata = s_metadata[:-4]  # Quito el .csv

    rules_filename = s_metadata

    re_family = re.compile("(.*)_len\d")   # Todo antes de "_len\d" es la familia
    family = re_family.findall(s_metadata)[0]
    s_metadata = s_metadata.replace(family, "", 1)  # Quito la familia

    md = s_metadata.split("_")
    min_len = md[1]
    
    if md[2] == "nomrs":
        transaction_type = md[2]
        maximal_repeat_type = None
        clean_mode = None
        min_support = md[3][1:] # Remove prefix "s"
        min_confidence = md[4][1:] # Remove prefix "c"
    else:
        transaction_type = "mrs"
        maximal_repeat_type = md[2]  
        clean_mode = md[3]
        min_support = md[4][1:] # Remove prefix "s"
        min_confidence = md[5][1:] # Remove prefix "c"


    return RuleMetadata(rules_filename, family, min_len, transaction_type, maximal_repeat_type, clean_mode, min_support, min_confidence)


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

    print("Reading rules file...")
    df_rules = build_df_rules_from_path(info_rules["path_rules"])

    print("Building rules from file...")
    rules = build_rule_list_from_df(df_rules)

    print("Calculating rules stats...")
    info_rules["rules_amount"] = len(rules)
    info_rules["rules_unique_items"] = len(set(itemset(rules)))
    info_rules["rules_unique_antecedents"] = len(set(antecedents(rules)))
    info_rules["rules_unique_consecuents"] = len(set(consequents(rules)))

    print("Classifying rules...")
    rules_str = list(df_rules["rules"])
    ruletypes = list(df_rules["ruletype"])

    info_rules["rules_type_add"] = len(ruletypes_with("Agrega", rules_str, ruletypes))
    info_rules["rules_type_overlap"] = len(ruletypes_with("Overlap", rules, ruletypes))
    info_rules["rules_type_n/a"] = len(ruletypes_with("N/A", rules_str, rules_str))

    print(df_rules.head())

    # for rt in ruletypes_with("N/A", rules, ruletypes):
    #     print(rt)

    # print("Reading transactions file...")
    # transactions = transactions_from_path(info_rules["path_transactions"])
    # print("Calculating transactions stats...")
    # txs_items = all_mrs_from_transactions(transactions)

    # info_rules["txs_amount"] = len(transactions)
    # info_rules["txs_items"] = len(txs_items)
    # info_rules["txs_unique_items"] = len(set(txs_items))

    return info_rules


import sys

if __name__ == '__main__':

    family = "NEWAnk"
    min_len = "len4"
    mr_type = "ALL_sub"
    min_support = "0.025"
    min_confidence = "0.9"

    if len(sys.argv) > 1:
        print("sys.argv", sys.argv)
        assert(len(sys.argv) == 6)
        family, min_len, mr_type, min_support, min_confidence = sys.argv[1:]

    info_rules = build_info_rules_for(family, min_len, mr_type, min_support, min_confidence)

    for k, v in info_rules.items():
        print(f"{k}: {v}")



