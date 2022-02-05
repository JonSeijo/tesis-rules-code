# logo_analysis
# ¿Tenés la cantidad de casos que estás usando para la construcción de esos logos? 
# ¿Y la cantidad de proteínas donde ocurre?

import argparse
import pathlib
import os
import re

parser = argparse.ArgumentParser(description='Logo analysis')

parser.add_argument('-sto_path',
    type=pathlib.Path,
    action='store',
    required=True,
    help='relative path to .sto files')

parser.add_argument('-sto',
    type=str,
    nargs='+', # 1 or more
    required=True,
    help='names of the consequents to analyse')

args = parser.parse_args()


path_sto = str(args.sto_path)
assert(path_sto[-1] != "/")

stos = args.sto

# -------------------------------------------
all_proteins = []
all_contexts = []
all_rules = []

info_by_sto = {}

def process_file(fullpath, dict_info):
    """ Reads the file received and process each line creating words """
    with open(fullpath, 'r') as infile:
        for line in infile:
            l = line.strip()
            if len(l) > 0 and (l[0] != '#' or l[0] != '//'): #Skip comments or file ending mark
                parts = re.split(r'\t+', l)
                if len(parts) > 1:
                    process_item(parts[0], parts[1], dict_info)


# Ojo, hay dos formatos:
#   AAKG-LHAA-AAAK-0-UniRef90_UPI00038F1754.fasta, ALAAAKGG
#   PLHL-VEVL-LHLA-0-UniRef90_Q8R516-2.fasta, TALHLAAL
def process_item(rule_protein, context, dict_info):
    splitted = rule_protein.split("-")
    protein = splitted[-1]

    right_rule_index = -3
    # TODO: Esto se rompe si considero MR de longitud 1. Posiblemente nunca quiera considerar eso igual.
    if len(splitted[right_rule_index]) == 1: # En este caso no es una regla, es el numero para diferenciar repeticion
        right_rule_index = -4

    left_rule = ",".join(sorted(splitted[:right_rule_index])) # IMPORTANT TO SORT, rules can be in any order
    
    # print(left_rule)
    right_rule = splitted[right_rule_index]
    rule = left_rule + " -> " + right_rule
    # print(rule)

    # TODO: Esto podria ser un item en si mismo en vez de agregarlo en tres listas separadas
    dict_info['all_proteins'].append(protein)
    dict_info['all_contexts'].append(context)
    dict_info['all_rules'].append(rule)

print(path_sto.split("/")[-1])

for sto in stos:

    info_by_sto[sto] = {
        'all_proteins': [],
        'all_contexts': [],
        'all_rules': [],
    }

    fullpath = os.path.join(path_sto, sto + ".sto")
    process_file(fullpath, info_by_sto[sto])

    d = info_by_sto[sto]

    print("----------------------------")
    print(sto)
    print("unique_rules:   ", len(set(d['all_rules'])))
    print()
    print("all_contexts:   ", len(d['all_contexts']))
    print("unique_contexts:", len(set(d['all_contexts'])))
    print()
    print("all_proteins:   ", len(d['all_proteins']))
    print("unique_proteins:", len(set(d['all_proteins'])))
    print()

    # print(set(all_rules))
