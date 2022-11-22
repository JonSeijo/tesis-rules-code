# python3
"""
Script para encapsular el transaction_cleaner de JM
"""

import argparse
import subprocess
import time
from datetime import timedelta
import pathlib
import sys
import os

from multiprocessing import Pool
from typing import List

PATH_JM_CODE = "main_code/"
PATH_DEFAULT_TXS = "output/transactions/"
PATH_DEFAULT_CLEAN_TXS = "output/clean_transactions/"

def map_str(ls) -> List[str]:
    return list(map(str, ls))

def show_posible_txs() -> None:
    print("-----------")
    print("Transactions in default location: ")
    txs_names = sorted([ fname for fname in os.listdir(PATH_DEFAULT_TXS)])
    for tx in txs_names:
        print(tx[:-4])
    print("-----------")

def validate_txs_names(path_input_dir, txs_names) -> None:
    output_dir_contents = os.listdir(path_input_dir)
    for tx_name in txs_names:
        if tx_name + ".csv" not in output_dir_contents:
            raise Exception(f"Cannot find '{tx_name}.csv' in path '{path_input_dir}'")


parser = argparse.ArgumentParser(description='Run tx-cleaner')

parser.add_argument('-txs',
    type=str,
    nargs='+', # 1 or more
    required=True,
    help='names of the transaction csv to clean')

parser.add_argument('--input_dir',
    type=pathlib.Path,
    action='store',
    help=f'relative path to input transactions directory. Default: {PATH_DEFAULT_TXS}',
    default=PATH_DEFAULT_TXS)

parser.add_argument('--output_dir',
    type=pathlib.Path,
    action='store',
    help=f'relative path to output clean transactions directory. Default: {PATH_DEFAULT_CLEAN_TXS}',
    default=PATH_DEFAULT_CLEAN_TXS)

parser.add_argument('--mode',
    type=str,
    choices=['minimum', 'substring', 'superstring'],
    help=' substring, superstring or minimum mode for cleaning.')

parser.add_argument('--threads',
    type=int,
    help=' amount of subprocesses for paralelization. Default=1',
    default=1)


parser.add_argument('-no_confirmation', action='store_true', help=' flag for continuing without confirmation')

# ------------------------------------------------

show_posible_txs()

args: argparse.Namespace = parser.parse_args()

path_input_dir = str(args.input_dir)
path_output_dir = str(args.output_dir)

ask_confirmation: bool = not args.no_confirmation

num_threads = args.threads

txs_names = args.txs

validate_txs_names(path_input_dir, txs_names)


executable = f"./{PATH_JM_CODE}cleaner"
str_mode = args.mode[:3]  # sub/sup/min

if args.mode == "substring":
    clean_mode = 0
elif args.mode == "superstring":
    clean_mode = 1
elif args.mode == "minimum":
    clean_mode = 2
else:
    raise Exception("Unexpected clean mode")

print("---------------------------------")
print("Running tx-cleaner with params:")
print("  executable:   ", executable)
print("  clean_mode:   ", (str_mode, clean_mode))
print("  input_dir:    ", path_input_dir)
print("  output_dir:   ", path_output_dir)
print("  txs_names:    ", txs_names)
print("                ")

# Ask for confirmation
if ask_confirmation:
    answer: str = input("-----\nContinue? YES/NO: ")
    if answer.upper() not in ["Y", "YE", "YES"]:
        sys.exit()
    print("\n\n\n")


# Makefile
print("Running tx-cleaner makefile in:", PATH_JM_CODE)
subprocess.run(["make", "cleaner"], cwd=PATH_JM_CODE)
print()


def execute_subprocess(tx_name) -> None:
    input_file = path_input_dir + "/" + tx_name + ".csv"
    output_file = path_output_dir + "/" + tx_name + "_" + str_mode + ".csv"
    # ------------------------------------------------

    # Clean transactions
    # ./tesis-jmenriquez-code/cleaner 
    #   maximal-repeats-transactions/output/transactions.csv 
    #   0 
    #   cleaned_0_transactions.csv
    print(f"----------------")
    print(f"Running tx-cleaner for {tx_name}")
    subprocess.run(map_str([executable, input_file, clean_mode, output_file]))


start_txgen: float = time.time()

with Pool(num_threads) as p:
    p.map(execute_subprocess, txs_names)

end_txgen: float = time.time()
print()
print(f"time for cleaning all txs:", str(timedelta(seconds=end_txgen-start_txgen)))