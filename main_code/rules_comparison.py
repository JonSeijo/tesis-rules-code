# rules_comparison.py
import pandas as pd

df_jonno = pd.read_csv("../association_rules_ALL_0.025.csv")
# df_jonno = pd.read_csv("../association_rules_NNNE_0.025.csv")
df_jm = pd.read_csv("rules_jmenriquez.csv", sep=";", header=None, names=["rules"])

# s = {GNTA,HLAA,NTAL,PLHL,TPLH}
def build_set(s):
	s = s[1:-1]
	ls = s.split(",")
	return set(ls)

# "{ALHV,LHIA} => {LHVA}"  ----> ({ALHV,LHIA}, {LHVA})
def from_str(rule_str):
	left, right = rule_str.split(" => ")
	return build_set(left), build_set(right)

def rule_list(df_rules):
	return [from_str(rule[0]) for idx, rule in df_rules[["rules"]].iterrows()]

rules_jonno = rule_list(df_jonno)
rules_jm = rule_list(df_jm)


# print(len(rules_jonno))
# print(len(rules_jm))
# print(rules_jm)
intersection = [ rule for rule in rules_jm if rule in rules_jonno ]
not_jm_rules = [ rule for rule in rules_jm if rule not in rules_jonno ]

print("rules_jm", len(rules_jm))
print("rules_jonno", len(rules_jonno))
print("intersection", len(intersection))
print("not_jm_rules", len(not_jm_rules))

# for l,r in not_jm_rules:
# 	print(f"{l} -> {r}")

