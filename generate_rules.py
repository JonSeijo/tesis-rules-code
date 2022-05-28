import csv

from efficient_apriori import apriori

import pandas as pd


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


# TODO: Parametrizar

family = "NEWAnk"
min_support = 0.025
min_confidence = 0.9

# PATH_RULES = "output/rules/"
PATH_RULES = "output/pyrules/"
PATH_TRANSACTIONS = "output/clean_transactions/"

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
    transactions, min_support=min_support, min_confidence=min_confidence)

print()
print("Removing rules with multiple consecuents...")
rules = [rule for rule in rules if len(rule.rhs)==1]

print()
print()
print("#rules:", len(rules))
print()
print("Ready!")

df_rules = rules_to_df(rules)

outname_rules = f"{PATH_RULES}{family}_len4_ALL_sub_s{min_support}_c{min_confidence}.csv" 

print("Writting rules to: ", outname_rules)
df_rules.to_csv(outname_rules, index=None, quoting=csv.QUOTE_NONNUMERIC)
