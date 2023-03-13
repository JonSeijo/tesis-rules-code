# tesis-code

# Estructura

- `maximal-repeats-transactions/`: repositorio para generar transacciones de maximal repeats a partir de una familia de proteinas. Codigo original de pturjanski

- `main_code`: generador de reglas, analisis posteriores y generador de db para el visualizador. Codigo principal de Enriquez.

- `protein-visualization`: docker y la aplicacion visualizadora, en otro repo.

- `experiments`: jupyter-notebooks con todos los experimentos de la tesis, en otro repo. 

# Setup

### R
- Instalar R y Rstudio
- sudo apt install r-base-dev
- sudo apt install libcurl4-openssl-dev libssl-dev

### Python
- python3 -m venv venv-tesis 
  : source venv-tesis/bin/activate
  : pip install -r requirements.txt

# Run

- Generar transacciones: `generate_transactions.py`

- Refinar transacciones: `clean_transactions.py`

- Generar reglas: `generate_rules.r`. Ejemplo: `./generate_rules.r --family=NEWAnk` (quiza necesite previamente `chmod u+x generate_rules.r`)

- Comparacion de reglas: `compare_rules.py`

- Generacion de logos:
  : run_parse_app
  : logo_maker.py

- Analisis de logos
```bash
python3 logo_analysis.py -sto_path tesis-jmenriquez-code/out_parse_rules_jonno_NEWAnk/ -sto GADV LHLA LISH TPLH > output/logos/logo_analysis_jonno_NEWAnk.txt
```

```bash
python3 logo_analysis.py -sto_path tesis-jmenriquez-code/out_parse_rules_jm_ank -sto GADV LHLA LISH TPLH > output/logos/logo_analysis_jm_ank.txt
```

- Generacion de db para visualizador: `rule_db_generator.py`

```bash
python3 -m rule_db_generator --protein_path=../db/canonicalFamilyDataset/familyDataset/TPR1/ --rule_file=output/rules/TPR1_len4_ALL_sub_s0.025_c0.9.csv --filename=output/dbs/db_test.db
``` 

- Visualizacion de proteínas: ver repo de visualizador.
