# Esto es un experimento para usar la libreria de python "apriori" para la generacion de reglas
# Tiene serios problemas de performance, usar la libreria de R,
# !!! usar ./generate_rules.r !!!

import argparse
import csv

from efficient_apriori import apriori

import pandas as pd

DEFAULT_MIN_SUPPORT = "0.025"
DEFAULT_MIN_CONFIDENCE = "0.9"

PATH_RULES = "output/pyrules/"
PATH_TRANSACTIONS = "output/clean_transactions/"

def rules_to_df(rules):
    rules_data = {
        "rules": [], "support": [], "confidence": [], "lift": []
    }

    def _pf(s):
        return "{" + ",".join(str(k) for k in s) + "}"

    for rule in rules:
        rules_data["rules"].append(f"{_pf(rule.lhs)} => {_pf(rule.rhs)}")
        rules_data["support"].append(rule.support)
        rules_data["confidence"].append(rule.confidence)
        rules_data["lift"].append(rule.lift)

    return pd.DataFrame(rules_data)


def generate(family: str, min_support: str, min_confidence: str, max_length: str, verbosity: str):

    filename_transactions = f"{PATH_TRANSACTIONS}{family}_len4_ALL_sub.csv"
    print("Reading transactions from:", filename_transactions)

    with open(filename_transactions) as file_transactions:
        transactions = [tx.strip().replace(" ", "").split(",") 
            for tx in file_transactions.readlines()]

    print("#transactions:", len(transactions))

    assert len(transactions) > 10000

    print()
    print("Running apriori with params:")
    print(" min_support:    ", min_support)
    print(" min_confidence: ", min_confidence)

    itemsets, rules = apriori(
        transactions, 
        min_support=float(min_support), 
        min_confidence=float(min_confidence),
        max_length=int(max_length),
        verbosity=int(verbosity))

    print()
    print("Removing rules with multiple consecuents...")
    rules = [rule for rule in rules if len(rule.rhs)==1]

    print()
    print()
    print("#rules:", len(rules))
    print()
    print("Ready!")

    return itemsets, rules

def save_to_csv(rules, family, min_support, min_confidence):
    print("Generating df...")
    df_rules = rules_to_df(rules)

    outname_rules = f"{PATH_RULES}{family}_len4_ALL_sub_s{min_support}_c{min_confidence}.csv" 

    print("Writting rules to: ", outname_rules)
    df_rules.to_csv(outname_rules, index=None, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generate rules')
    
    parser.add_argument('family',
        type=str,
        help='Protein family to generate rules. For example: ank/NEWAnk/TPR1/LRR1. Case sensitive!')


    parser.add_argument('--min_support',
        type=str,
        action='store',
        help=f'min_support for apriori algorithm (default={DEFAULT_MIN_SUPPORT})',
        default=DEFAULT_MIN_SUPPORT,
    )

    parser.add_argument('--min_confidence',
        type=str,
        action='store',
        help=f'min_confidence for apriori algorithm (default={DEFAULT_MIN_CONFIDENCE})',
        default=DEFAULT_MIN_CONFIDENCE,
    )

    parser.add_argument('--max_length',
        type=str,
        action='store',
        help=f'max_length for rules/itemsets apriori algorithm (default=8)',
        default="8",
    )

    parser.add_argument('--verbosity',
        type=str,
        action='store',
        help=f'verbosity for apriori algorithm [0|1|2] (default=1)',
        default="1",
    )

    args = parser.parse_args()

    family = args.family
    min_support = args.min_support
    min_confidence = args.min_confidence
    max_length = args.max_length
    verbosity = args.verbosity

    itemsets, rules = generate(family, min_support, min_confidence, max_length, verbosity)

    # Mejor usa /generate_rules.r!
    # save_to_csv(rules, family, min_support, min_confidence)
