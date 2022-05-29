# tesis-code

# Estructura

 #TODO: repensar y reorganizar codigo existente

- `maximal-repeats-transactions/`: repositorio para generar transacciones de maximal repeats a partir de una familia de proteinas. 

- `main-code`: generador de reglas, analisis posteriores y generador de db para el visualizador. #TODO: subdivisiones

- `protein-visualization`: docker y la aplicacion visualizadora en si.


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

- Limpiar transacciones: `clean_transactions.py`

- Generar reglas: `generate_rules.r`. Ejemplo: `./generate_rules.r --family=NEWAnk` (quiza necesite previamente `chmod u+x generate_rules.r`)

- Simplificar output reglas: `simplify_rules_format.py`

- Comparar reglas: `compare_rules.py`

- Generacion de logos:
  : run_parse_app
  : logo_maker.py

- Analisis de logos
```python3 logo_analysis.py -sto_path tesis-jmenriquez-code/out_parse_rules_jonno_NEWAnk/ -sto GADV LHLA LISH TPLH > output/logos/logo_analysis_jonno_NEWAnk.txt```

```python3 logo_analysis.py -sto_path tesis-jmenriquez-code/out_parse_rules_jm_ank -sto GADV LHLA LISH TPLH > output/logos/logo_analysis_jm_ank.txt```

