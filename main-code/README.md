## Setup

Instalar libreria `boost` para c++

```bash
sudo apt install libboost-all-dev
```



## Ejemplo de uso

Modo 0 es modo substring

```bash
make cleaner
time ./tesis-jmenriquez-code/cleaner maximal-repeats-transactions/output/transactions.csv 0 cleaned_0_transactions.csv
```



# Generador de db

```bash
time python3 rulegroup/rule_db_generator.py --proteinPath=../../db/canonicalFamilyDataset/familyDataset/TPR1/ --ruleFile=../output/simplified_rules/TPR1_len4_ALL_sub_s0.015_c0.75..txt
```

```bash
time python3 rulegroup/rule_db_generator.py --proteinPath=../../db/canonicalFamilyDataset/familyDataset/NEWAnk/ --ruleFile=../output/simplified_rules/NEWAnk_len4_ALL_sub_s0.02_c0.9..txt 
```