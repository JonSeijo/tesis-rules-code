import argparse
import pathlib
import pandas as pd

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

rules_a = rule_list(df_a)
rules_b = rule_list(df_b)


# print(len(rules_a))
# print(len(rules_b))
# print(rules_b)
intersection = [ rule for rule in rules_b if rule in rules_a ]
rules_in_b_not_in_a = [ rule for rule in rules_b if rule not in rules_a ]
rules_in_a_not_in_b = [ rule for rule in rules_a if rule not in rules_b ]


print()
print()
print()
print("rules_a:", path_rules_a.split("/")[-1])
print("rules_b:", path_rules_b.split("/")[-1])
print()
print("#rules_a:", len(rules_a))
print("#rules_b:", len(rules_b))
print()
print("#intersection:", len(intersection))
print("#rules_in_b_not_in_a:", len(rules_in_b_not_in_a))
print("#rules_in_a_not_in_b:", len(rules_in_a_not_in_b))
print()
print()

# for l,r in rules_in_a_not_in_b:
# 	print(f"{l} -> {r}")


# Pequeña exploracion:
# for l, r in rules_a:
# 	mayor_4 = False
# 	for x in l:
# 		if len(x) >	 4:
# 			mayor_4 = True
# 	for x in r:
# 		if len(x) > 4:
# 			mayor_4 = True

# 	if mayor_4:
# 		print(f"{l} -> {r}")
