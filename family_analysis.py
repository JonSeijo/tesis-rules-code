import os
from typing import List

from utils import list_valid_families

from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"]= (8, 6)

PATH_DATASETS_SINGLE = "output/family_datasets"

# TODO: Documentar uso del migrate_proteins.py para este tipo de lectura
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

# Build DataFrame with all proteins info for every family
def build_df_families_proteins(families):
    families_protein_data = {
        "family": [],
        "protein_name": [],
        "protein_len": []
    }

    for family in families:
        proteins = read_db_single(family, silent_output=True)
        for p in proteins:
            families_protein_data["family"].append(family)
            families_protein_data["protein_name"].append(p.name)
            families_protein_data["protein_len"].append(len(p.seq))

    return pd.DataFrame(families_protein_data)

if __name__ == '__main__':

    print(sorted(list_valid_families(PATH_DATASETS_SINGLE)))

    families = ["NEWAnk", "TPR1"]
    df_families_proteins = build_df_families_proteins(families)

    df_families_proteins.boxplot(column='protein_len', by='family', grid=True)
    df_families_proteins.groupby('family').count().plot(kind='bar', y='protein_name', label='Cantidad de proteinas', grid=True)

    plt.show()
