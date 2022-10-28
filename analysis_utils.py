# transactions_analysis.py
import os
from collections import defaultdict
from typing import Dict, List, Set

import pandas as pd


# TODO: Testing. Dividir construccion de dict de dataframe.

def read_clean_transactions(
    family: str, transactions_path="output/clean_transactions"
) -> List[List[str]]:
    path_mr = os.path.join(transactions_path, f"{family}.csv")

    with open(path_mr) as mr_file:
        transactions = [tx.strip().replace(" ", "").split(",") for tx in mr_file.readlines()]
        return transactions


def build_transaction_len_df(txs_from_family: Dict[str, List[List[str]]]): # TODO: Transaction type
    txs_len_data = { "family": [], "tx_length": [] }
    for family, txs in txs_from_family.items():
        print(f"Building transaction_len_df for {family}")
        for tx in txs:
            txs_len_data["family"].append(family)
            txs_len_data["tx_length"].append(len(tx))

    return pd.DataFrame(txs_len_data)


def build_mr_len_df(mrs_from_family: Dict[str, Set[str]]):
    mrs_len_data = { "family": [], "mr_length": [] }
    for family_name, mrs in mrs_from_family.items():
        print(f"Building mr_len_df for {family_name}")
        for mr in mrs:
            mrs_len_data["family"].append(family_name)
            mrs_len_data["mr_length"].append(len(mr))
            
    return pd.DataFrame(mrs_len_data)


# mr frecuencies considering the amount of txs it appears 
def build_mr_tx_frequency_df(
    txs_from_family: Dict[str, List[List[str]]] 
):
    mrs_freq_data = { "family": [], "mr": [], "freq": [], "freq_percentage": [] }
    for family, transactions in txs_from_family.items():
        print(f"Building mr_tx_frequency for {family}")
        
        freq_by_mr = tx_frequencies_by_item(transactions)
        for mr, freq in freq_by_mr.items():
            mrs_freq_data["mr"].append(mr)
            mrs_freq_data["freq"].append(freq)
            mrs_freq_data["family"].append(family)
            mrs_freq_data["freq_percentage"].append(freq / len(transactions))

    print("Finished")
    return pd.DataFrame(mrs_freq_data) 


"""
Esto tarda varios minutos. Para cada transaccion mira todos los pares de elementos.

Algoritmo naive: para cada par de items posible, itero sobre las transacciones para contar
 Esto NO funciona, es demasiado lento.
La clave es que la gran mayoria de las transacciones no van a tener a ese par
y la cantidad de pares es aprox 2000*2000

Algoritmo usado: 
 - Primero elimino de las transacciones todos los mrs que no superan el min_support
  De esa forma las transacciones ahora me quedan de largo promedio 100
 - Para cada transaccion, sumo 1 a cada combinacion de SUS pares de items en un hashmap general
  Esto significa que unicamente considero pares que estan presentes en las transacciones
"""
def build_pairs_mr_tx_frequency_df(
    txs_from_family: Dict[str, List[List[str]]],
    mr_tx_frequency_df: pd.DataFrame,
    min_support: float
):

    frequent_mrs_by_family = build_frequent_mrs_by_family(mr_tx_frequency_df, min_support)

    freq_by_pair_data = {  "item_pair": [], "freq": [], "freq_percentage": [], "family": [] }
    
    for family, transactions in txs_from_family.items():
        
        if family in frequent_mrs_by_family:
            family_frequent_mrs = frequent_mrs_by_family[family] 
        else:
            print(f"WARNING! No frequent mrs for family: {family}")
            family_frequent_mrs = {}

        print(f"Building freqs_by_pair_combinations for {family}...")
        freq_by_pair = get_freqs_by_pair_combinations(family_frequent_mrs, transactions)
        
        print(f"Building freqs_by_pair_data for {family}...")
        for itempair, frequency in freq_by_pair.items():
            freq_by_pair_data["item_pair"].append(itempair)
            freq_by_pair_data["freq"].append(frequency)
            freq_by_pair_data["freq_percentage"].append(frequency / len(transactions))
            freq_by_pair_data["family"].append(family)
        print(f"{family} ready.")
        
    return pd.DataFrame(freq_by_pair_data)

# mrs: deberian ser los items frecuentes para que tenga sentido la optimizacion
def get_freqs_by_pair_combinations(mrs, transactions): 
    print("Filtering transactions_frequents")
    # Me quedo solo con los items frecuentes de las transacciones,
    #  porque no tiene sentido iterar por los no-frecuentes
    transactions_frequents = get_transactions_with_frequents(mrs, transactions)

    # freq_by_pair = {}
    freq_by_pair = defaultdict(int)

    for t_index, tx in enumerate(transactions_frequents):
        if t_index % 10000 == 0:
            print(f" .... {t_index}/{len(transactions_frequents)}")

        for i in range(len(tx)):
            item_a = tx[i]
            for j in range(i+1, len(tx)):
                item_b = tx[j]
                # key = item_a + "_" + item_b

                # Solo cuento el orden (a,b) porque las tx vienen ordenadas!
                freq_by_pair[item_a + "_" + item_b] += 1
    return freq_by_pair
                
# Para que me de la complejidad, primero elimino de las transacciones los elementos que no superan el minsupport
def get_transactions_with_frequents(mrs, transactions):
    transactions_frequents = []
    for tx in transactions:
        trans_curr = [item for item in tx if item in mrs]
        transactions_frequents.append(trans_curr)    
    return transactions_frequents

def build_frequent_mrs_by_family(mr_tx_frequency_df: pd.DataFrame, min_support: float):
    # TODO: Esto puede hacerse sin un .itertuples, con un df count por ej

    print("build_pairs_mr_tx_frequency_df, min_support:", min_support)
    df_only_frequents = mr_tx_frequency_df[ mr_tx_frequency_df.freq_percentage > min_support ]

    print("Filtering mrs to get most frequents only")    
    frequent_mrs_by_family = {}
    for row in df_only_frequents.itertuples():
        frequent_mrs_by_family[row.family] = frequent_mrs_by_family.get(row.family, set())
        frequent_mrs_by_family[row.family].add(row.mr)

    return frequent_mrs_by_family


def tx_frequencies_by_item(txs: List[List[str]]):
    # Para cada mr, su frecuencia
    mr_freqs = {}
    for i, tx in enumerate(txs):
        if i % 10000 == 0:
            print(f" .... freq_count .... {i}/{len(txs)}")
            
        for mr in tx:
            mr_freqs[mr] = mr_freqs.get(mr, 0) + 1
    return mr_freqs


if __name__ == "__main__":
    print("Transactions analysis.")
    print("TODO: Migrate from jupyter")