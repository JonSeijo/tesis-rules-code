import analysis_utils as autils

from compare_rules import fast_list_intersection, all_mrs_from_transactions

from typing import List

def exp_0_intersection(
    family_a_name: str, mrs_a: List[str], family_b_name: str, mrs_b: List[str]
) -> List[str]:
    """
    A partir de una lista con todos los MRs de una familia, con repetidos!
    Calculo la interseccion
    """
    print("Running exp0...")

    exp0_intersection = fast_list_intersection(mrs_a, mrs_b)

    print("========================")
    print("exp_0_intersection")
    print(f"{family_a_name} total:     ", len(mrs_a))
    print(f"{family_b_name} total:     ", len(mrs_b))
    print("result intersection: ", len(exp0_intersection))
    print("========================")


def _sanity_check(txs):
     # Sanity check: cada transaccion no tiene items repetidos
    for idx, transaccion in enumerate(txs):
        for tx in transaccion:
            if len(tx) != len(set(tx)):
                raise Exception("Transaccion invalida!")
        print(f"Check transactions {idx} .. OK!")

if __name__ == '__main__':
    # Traido del jupyter
    
    # Ejemplo de uso    
    transactions_newank = autils.read_clean_transactions("NEWAnk_len4_ALL_sub", "output/clean_transactions")
    transactions_tpr = autils.read_clean_transactions("TPR1_len4_ALL_sub", "output/clean_transactions")

    assert len(transactions_newank) == 32169
    assert len(transactions_tpr) == 36389

    _sanity_check([transactions_newank, transactions_tpr])

    mrs_newank = all_mrs_from_transactions(transactions_newank)
    mrs_tpr = all_mrs_from_transactions(transactions_tpr)

    mrs_newank_unique = set(mrs_newank)
    mrs_tpr_unique = set(mrs_tpr)

    exp_0_intersection("NEWAnk", mrs_newank, "TPR1", mrs_tpr)

