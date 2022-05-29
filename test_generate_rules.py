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

def test_output_csv(family, support, confidence):
    filename_rules = f"{family}_len4_ALL_sub_s{support}_c{confidence}.csv"

    filename_rules_r = f"output/rules/{filename_rules}"
    rules_r = build_rules(filename_rules_r)

    filename_rules_py = f"output/pyrules/{filename_rules}"
    rules_py = build_rules(filename_rules_py)

    # print("     len(rules_r) :", len(rules_r))
    # print("     len(rules_py):", len(rules_py))
    assert len(rules_r) == len(rules_py)

    differences = []
    for r, py in zip(rules_r, rules_py):
        if r != py:
            differences.append((r, py))

    if len(differences) == 0:
        print(f"{family}: ALL OK!!!")
    else:
        print(f"{family}: #differences: ", len(differences))
        # for r, py in differences:
        #     print(r)
        #     print(py)
        #     print()
    print()

if __name__ == '__main__':
    test_output_csv("NEWAnk", 0.025, 0.9)
    test_output_csv("TPR1", 0.025, 0.9)

    print("LRR1: Problemas!!! En R hay una forma de hacer timeout, que permite que genere reglas de largo 3 sin que explote. En python es todas las de 3 o nada, y necesita infinitos recursos\n")
    # test_output_csv("LRR1", 0.025, 0.9)
