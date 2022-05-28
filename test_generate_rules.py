# Aca veo que las reglas generadas por "generate_rules.py"
#  son exactamente las mismas que las de "generate_rules.R"

import math
import pandas as pd

class Rule:
    def __init__(self, rule, support, confidence, lift):
        self.rule = self._normalized_rule(rule) # Components of the rule are sets
        self.support = support
        self.confidence = confidence
        self.lift = lift

    def _normalized_rule(self, rule):
        arrow = " => "
        left_s, right_s = rule.split(arrow)
        
        def sorted_items(items_s):
            items = items_s[1:-1].split(',')  # Quito los { }
            items = sorted(items)
            return "{" + ",".join(items) + "}"

        return sorted_items(left_s) + arrow + sorted_items(right_s)


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return (self.rule == other.rule 
            and math.isclose(self.support, other.support)
            and math.isclose(self.confidence, other.confidence)
            and math.isclose(self.lift, other.lift))

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))

    def __ne__(self, other):
        return not self.__eq__(other)


def build_rules(filename):
    rules = []
    df = pd.read_csv(filename)
    for row in df.itertuples():
        rule = Rule(row.rules, row.support, row.confidence, row.lift)
        rules.append(rule)

    return sorted(rules, 
        reverse=True, 
        key=lambda rule: (rule.support, rule.confidence, rule.lift, rule.rule))

filename_rules_r = "output/rules/NEWAnk_len4_ALL_sub_s0.025_c0.9.csv"
rules_r = build_rules(filename_rules_r)

filename_rules_py = "output/pyrules/NEWAnk_len4_ALL_sub_s0.025_c0.9.csv"
rules_py = build_rules(filename_rules_py)

assert len(rules_r) == len(rules_py)

differences = []
for r, py in zip(rules_r, rules_py):
    if r != py:
        differences.append((r, py))

if len(differences) == 0:
    print("ALL OK!!!")
else:
    print("#differences: ", len(differences))
    for r, py in differences:
        print(r)
        print(py)
        print()


