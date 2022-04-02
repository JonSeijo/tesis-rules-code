# Experimento 4

Se computaron los MRs para 70869 proteínas de la familia _mixScrambled_ en dos formas. Aquellos
de longitud mayor o igual a 4 con dos modos de calcular los MR: *bag* y *proteína a proteína*.

Con esto se armaron _transacciones_, es decir, para cada proteína tomamos los MRs que estuvieran presentes
en estas y generamos items para poder alimentar el algoritmo de generación de reglas de negocio
para utilizar la técnica de _Market Basket Analysis_.

```bash
./txmba_bag ../../data/proteins/familyDataset/mixScrambled/ - 4 1 70869 scrambled-mr4.txt
```

#### Ensayo 1: MR modo Bag

-  Min long de MR: 4
-  Min Confidence: 0.9
-  Min Support: 0.0025 (Corte mínimo en 177 apariciones)
Y con estos parámetros obtenemos 766 reglas de asociación

#### Ensayo 2: MR Modo Bag - Exclusion

```
rules <- apriori(tx, parameter = list(support=0.005, confidence = 0.15, minlen = 2, maxtime = 30))
```
Parameter specification:
 confidence minval smax arem  aval originalSupport maxtime support minlen maxlen target   ext
       0.15    0.1    1 none FALSE            TRUE      30   0.005      2     10  rules FALSE

Algorithmic control:
 filter tree heap memopt load sort verbose
    0.1 TRUE TRUE  FALSE TRUE    2    TRUE

Absolute minimum support count: 354 

-  Min long de MR: 4
-  Min Confidence: 0.2
-  Min Support: 0.005 (Corte mínimo en 354 apariciones)
Y con estos parámetros obtenemos 54 reglas de asociación

#### Ensayo 3: MR Modo Bag - Inclusion

-  Min long de MR: 4
-  Min Confidence: 0.1
-  Min Support: 0.0000989 (Corte mínimo en 7 apariciones)
Y con estos parámetros obtenemos 0 (8904 ítems analizados) reglas de asociación

```
rules <- apriori(tx, parameter = list(support=0.0000989, confidence = 0.1, minlen = 2))
```