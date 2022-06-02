# python3

import argparse
import subprocess
import time
from datetime import timedelta
import pathlib
import sys
from typing import List

DIR_MAXIMAL_REPEATS_GENERATOR = "maximal-repeats-transactions/"
PATH_DEFAULT_FAMILY_DATASET = "../db/canonicalFamilyDataset/familyDataset"
DEFAULT_MIN_LEN = 4
DEFAULT_MAX_LEN = 999999
DEFAULT_MIN_PROTEINS = 1

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
    help='min length for maximal repeat (default=4)',
    default=DEFAULT_MIN_LEN,
)

parser.add_argument('--max_len',
    type=int,
    action='store',
    help='max length for maximal repeat (default=999999)',
    default=DEFAULT_MAX_LEN,
)

parser.add_argument('--min_proteins',
    type=int,
    action='store',
    help='min protein aparition for maximal repeat (default=1)',
    default=DEFAULT_MIN_PROTEINS,
)

parser.add_argument('-no_confirmation', action='store_true', help=' flag for continuing without confirmation')

# ------------------------------------------------

args: argparse.Namespace = parser.parse_args()

family = args.family

path_family_db = str(args.path_db)
assert(path_family_db[-1] != "/")

min_len = args.min_len
max_len = args.max_len
min_proteins = args.min_proteins

ask_confirmation: bool = not args.no_confirmation

executable = f"./{DIR_MAXIMAL_REPEATS_GENERATOR}tx-generator"
input_dir = path_family_db + "/" + family
output_prefix = f"output/transactions/{family}_len{min_len}"

# ------------------------------------------------


# time ./tx-generator ank ../../db/canonicalFamilyDataset/familyDataset/ank/ output/ank_min4 4 999999 1
print("---------------------------------")
print("Running tx-generator with params:")
print("  executable:   ", executable)
print("  family:       ", family)
print("  input_db:     ", input_dir)
print("  output_prefix:", output_prefix)
print("  min_len:      ", min_len)
print("  max_len:      ", max_len)
print("  min_proteins: ", min_proteins)
print("                ")

# Ask for confirmation
if ask_confirmation:
    answer: str = input("-----\nContinue? YES/NO: ")
    if answer.upper() not in ["Y", "YE", "YES"]:
        sys.exit()
    print("\n\n\n")


# Makefile
print("Running makefile in:", DIR_MAXIMAL_REPEATS_GENERATOR)
subprocess.run(["make"], cwd=DIR_MAXIMAL_REPEATS_GENERATOR)

# Generate transactions
print("Running tx-generator...")
start_txgen: float = time.time()
subprocess.run(map_str([executable, family, input_dir, output_prefix, min_len, max_len, min_proteins]))
end_txgen: float = time.time()

print()
print("time: ", str(timedelta(seconds=end_txgen-start_txgen)))
