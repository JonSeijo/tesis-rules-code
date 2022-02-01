# simplify_rules_format.py
# File for jm rule parser need specific file format, this is to convert the csv to a list of rules
import os

import pandas as pd

root = "output/rules/"
outroot = "output/simplified_rules/"
rules_files = os.listdir(root)

for filename in rules_files:
    fullpath = os.path.join(root, filename)
    out_filename = os.path.join(outroot, filename[:-3] + ".txt")

    df = pd.read_csv(fullpath)
    try:
        rules = list(df['rules'])
    except KeyError:
        print("ERROR. No rules in: ", fullpath, "    ignoring file")
        continue
        # print(rules)

    with open(out_filename, 'w') as f:
        for rule in rules:
            f.write("%s\n" % rule)
    print("OK. ", out_filename)

