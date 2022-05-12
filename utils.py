import os

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
