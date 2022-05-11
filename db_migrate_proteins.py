import os

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

PATH_DATASETS_MULTIPLE = "../db/canonicalFamilyDataset/familyDataset"
PATH_DATASETS_SINGLE = "output/family_datasets"

def read_db_multiples(family_name):
    path_input = os.path.join(PATH_DATASETS_MULTIPLE, family_name)
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


def write_db_single(proteins, family_name):
    filename_out = f"{PATH_DATASETS_SINGLE}/{family_name}.fasta"
    print(f"Writing db of proteins to single file: {filename_out}")
    with open(filename_out, "w") as output_handle:
        SeqIO.write(proteins, output_handle, "fasta")

# "NEWAnk"
def migrate_dataset(family_name):
    proteins = read_db_multiples(family_name)
    write_db_single(proteins, family_name)

def is_invalid_family(family_name):
    family_name = family_name.lower()
    for needle in ["uniform", "scrambled", "without", "_", "mix"]:
        if needle in family_name:
            return True
    return False

def valid_families(families):
    return [ family_name for family_name in families if not is_invalid_family(family_name) ]

if __name__ == '__main__':
    dataset_names = os.listdir(PATH_DATASETS_MULTIPLE)
    families = valid_families(dataset_names)

    for family_name in families:
        print(f"Migrating {family_name}")
        # migrate_dataset(family_name)

