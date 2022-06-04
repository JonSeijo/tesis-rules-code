import os

from typing import List

from Bio import SeqIO


def read_db_multiples(family_name, datasets_multiple_path):
    path_input = os.path.join(datasets_multiple_path, family_name)
    proteins = []

    curr_amount = 0
    for filename_protein in os.listdir(path_input):
        curr_amount += 1
        if curr_amount % 1000 == 0:
            print(f"Reading proteins from {path_input}: {curr_amount}")

        path_protein = os.path.join(path_input, filename_protein)
        protein = SeqIO.read(path_protein, "fasta")  # read -> the one and only protein
        proteins.append(protein)
    return proteins

def list_valid_families(dataset_path):
    dataset_names = os.listdir(dataset_path)
    dataset_names = [name.replace(".fasta", "") for name in dataset_names]
    return valid_families(dataset_names)

def is_invalid_family(family_name):
    family_name = family_name.lower()
    for needle in ["uniform", "scrambled", "without", "_", "mix"]:
        if needle in family_name:
            return True
    return False

def valid_families(families):
    return [ family_name for family_name in families if not is_invalid_family(family_name) ]
