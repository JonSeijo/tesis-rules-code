# Script para migrar las proteinas .fasta
# a un unico archivo .fasta con todas las proteinas

import os

from family_analysis import list_valid_families, read_db_multiples

from Bio import SeqIO

PATH_DATASETS_MULTIPLE = "../db/canonicalFamilyDataset/familyDataset"
PATH_DATASETS_SINGLE = "output/family_datasets"

def write_db_single(proteins, family_name):
    filename_out = f"{PATH_DATASETS_SINGLE}/{family_name}.fasta"
    print(f"Writing db of proteins to single file: {filename_out}")
    with open(filename_out, "w") as output_handle:
        SeqIO.write(proteins, output_handle, "fasta")

# "NEWAnk"
def migrate_dataset(family_name):
    proteins = read_db_multiples(family_name, PATH_DATASETS_MULTIPLE)
    write_db_single(proteins, family_name)

if __name__ == '__main__':
    families = list_valid_families(PATH_DATASETS_MULTIPLE)

    for family_name in families:
        print(f"Migrating {family_name}")
        # migrate_dataset(family_name)
