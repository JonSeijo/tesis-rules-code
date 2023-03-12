import os
from typing import List

from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"]= (8, 6)

PATH_DATASETS_SINGLE = "output/family_datasets"
PATH_DEFAULT_FAMILY_DATASET = "../db/canonicalFamilyDataset/familyDataset"


# Build DataFrame with all proteins info for every family
def build_df_families_proteins(families):
    families_protein_data = {
        "family": [],
        "protein_name": [],
        "protein_len": []
    }

    for family in families:
        proteins = read_db_multiples(family, PATH_DEFAULT_FAMILY_DATASET)
        for p in proteins:
            families_protein_data["family"].append(family)
            families_protein_data["protein_name"].append(p.name)
            families_protein_data["protein_len"].append(len(p.seq))

    return pd.DataFrame(families_protein_data)

# Cargar proteinas usando un unico .fasta con todas las secuencias juntas
# Ver migrate_proteins.py
def read_db_single(family_name: str, path_datasets=PATH_DATASETS_SINGLE, silent_output=False):
    proteins = []
    curr_amount = 0
    path_proteins = os.path.join(path_datasets, f"{family_name}.fasta")
    for protein in SeqIO.parse(path_proteins, "fasta"):  # parse -> multiple proteins
        curr_amount += 1
        if not silent_output and curr_amount % 1000 == 0:
            print(f"Reading proteins from {path_proteins}: {curr_amount}")
        proteins.append(protein)
    
    return proteins

# Carga proteinas usando formato estandar de un .fasta por cada secuencia
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


if __name__ == '__main__':

    print(sorted(list_valid_families(PATH_DATASETS_SINGLE)))

    families = ["NEWAnk", "TPR1"]
    df_families_proteins = build_df_families_proteins(families)

    df_families_proteins.boxplot(column='protein_len', by='family', grid=True)
    df_families_proteins.groupby('family').count().plot(kind='bar', y='protein_name', label='Cantidad de proteinas', grid=True)

    plt.show()
