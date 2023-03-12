# python3
# Generate transactions without using MRs (KMERAS/nomrs)
# It uses all substrings of length K instead

import argparse
import csv
import subprocess
import time
from datetime import timedelta
import pathlib
import sys
import os

from typing import List

from family_analysis import read_db_multiples


PATH_TRANSACTIONS = "output/clean_transactions/"
PATH_DEFAULT_FAMILY_DATASET = "../db/canonicalFamilyDataset/familyDataset"
DEFAULT_SUBSTRING_LEN = 4

def map_str(ls) -> List[str]:
    return list(map(str, ls))

parser = argparse.ArgumentParser(description='Run tx-generator')

parser.add_argument('family',
    type=str,
    help='protein family to generate transactions, for example: ank/NEWAnk/TPR1)')

parser.add_argument('--path_db',
    type=pathlib.Path,
    action='store',
    help='relative path to familyDataset db',
    default=PATH_DEFAULT_FAMILY_DATASET)

parser.add_argument('--min_len',
    type=int,
    action='store',
    help='length for substring (default=4)',
    default=DEFAULT_SUBSTRING_LEN,
)

parser.add_argument('-no_confirmation', action='store_true', help=' flag for continuing without confirmation')

# ------------------------------------------------

args: argparse.Namespace = parser.parse_args()

family = args.family

path_family_db = str(args.path_db)
assert(path_family_db[-1] != "/")

substring_len = int(args.min_len)

ask_confirmation: bool = not args.no_confirmation

output_prefix = os.path.join(PATH_TRANSACTIONS, f"{family}_len{substring_len}_nomrs")

# ------------------------------------------------

print("---------------------------------")
print("Running no-mrs transactions generator with params:")
print("  family:        ", family)
print("  path_family_db:", path_family_db)
print("  output_prefix: ", output_prefix)
print("  substring_len: ", substring_len)
print("                 ")

# Ask for confirmation
if ask_confirmation:
    answer: str = input("-----\nContinue? YES/NO: ")
    if answer.upper() not in ["Y", "YE", "YES"]:
        sys.exit()
    print("\n\n\n")


# Generate transactions
print("Running generator...")
start_txgen: float = time.time()

# TODO: test
def unique_substrings_with_len(protein_str: str, expected_len: int) -> List[str]:
    subs = set()
    for i in range(len(protein_str)):
        psub = protein_str[i:i+expected_len]
        if len(psub) == expected_len:
            subs.add(psub)
    return sorted(list(subs))

# Leer proteinas de los .fasta
proteins = read_db_multiples(family, path_family_db)

txs = []
for ip, protein in enumerate(proteins):
    if (ip % 1000 == 0):
        print(f" Generating tx for protein: {ip}")

    tx = unique_substrings_with_len(str(protein.seq), substring_len)
    txs.append(tx)

print(f"Writting to {output_prefix}.csv")
# Output: cada linea una transaccion, items separados por comas
with open(f"{output_prefix}.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(txs)

end_txgen: float = time.time()

print("Ready!")
print()
print("time: ", str(timedelta(seconds=end_txgen-start_txgen)))
