## Experimento 2

Se computaron los MRs para 38051 proteínas de la familia _Ankyrin_ en dos formas. Aquellos
de longitud mayor o igual a 4 con dos modos de calcular los MR: *bag* y *proteína a proteína*.

Con esto se armaron _transacciones_, es decir, para cada proteína tomamos los MRs que estuvieran presentes
en estas y generamos items para poder alimentar el algoritmo de generación de reglas de negocio
para utilizar la técnica de _Market Basket Analysis_.

```bash
./txmba_bag ./cosas-tesis-escritorio/data/proteins/familyDataset/ank/ - 4 1 38051 ank-mr4.txt
```

#### Ensayo 1: MR modo Bag

-  Min long de MR: 4
-  Min Confidence: 0.9
-  Min Support: 0.06 (Corte mínimo en 2283 apariciones)
Y con estos parámetros obtenemos 1223 reglas de asociación

#### Ensayo 2: MR Modo Bag - Exclusion (substring)

-  Min long de MR: 4
-  Min Confidence: 0.9
-  Min Support: 0.025 (Corte mínimo en 951 apariciones)
Y con estos parámetros obtenemos 394 reglas de asociación

(Exclusión: quita los MRs más largos dejando los más chicos)
**Este es el que utilizamos luego a lo largo del proyecto**

```
rules <- apriori(tx, parameter = list(support=0.025, confidence = 0.9, minlen = 2, maxlen = 6, maxtime = 30))
```

#### Ensayo 3: MR Modo Bag - Inclusion

No se pudieron generar datos. Este modo me deja en cada transacción los MRs de mayor longitud. Evidentemente
son muy poco comunes (ver txs-ank-ex-bag-25freq)

(Inclusión: quita los MRs más pequeños dejando los más largos)

#### Ensayo 4: MR Modo Protein - Exclusion

```
 rules <- apriori(tx, parameter = list(support=0.003, confidence = 0.85, minlen = 2, maxlen = 8))
```

-  Min long de MR: 4
-  Min Confidence: 0.85
-  Min Support: 0.003 (Corte mínimo en 98 apariciones)
Y con estos parámetros obtenemos 395 reglas de asociación

(Exclusión: quita los MRs más largos dejando los más chicos)

#### Ensayo 5: MR Modo Protein - Inclusion

```
rules <- apriori(tx, parameter = list(support=0.0022, confidence = 0.85, minlen = 2, maxlen = 8))
```

-  Min long de MR: 4
-  Min Confidence: 0.85
-  Min Support: 0.0022 (Corte mínimo en 72 apariciones)
Y con estos parámetros obtenemos 235 reglas de asociación

(Inclusión: quita los MRs más pequeños dejando los más largos)