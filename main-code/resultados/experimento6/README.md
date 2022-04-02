## Experimento 6

Vamos a probar qué sucede con los parámetros que usamos para generar
reglas de MBA para ANK con otros dos sets de datos: Ank Uniform (misma
longitud de proteínas pero tomados los aminoácidos de una distribución uniforme)
y Ank Scrambled (que consiste en hacer un shuffle de las proteínas Ank).

Parámetros originales para Ank Exclusion
-  Min long de MR: 4
-  Min Confidence: 0.9
-  Min Support: 0.025 (Corte mínimo en 951 apariciones)
(Exclusión: quita los MRs más largos dejando los más chicos)

#### Ensayo 1: MR Modo Bag - Exclusion - Scrambled

> rules <- apriori(tx, parameter = list(support=0.025, confidence = 0.9, minlen = 2))
Apriori

Parameter specification:
 confidence minval smax arem  aval originalSupport maxtime support minlen maxlen target   ext
        0.9    0.1    1 none FALSE            TRUE       5   0.025      2     10  rules FALSE

Algorithmic control:
 filter tree heap memopt load sort verbose
    0.1 TRUE TRUE  FALSE TRUE    2    TRUE

Absolute minimum support count: 951 

set item appearances ...[0 item(s)] done [0.00s].
set transactions ...[159765 item(s), 38051 transaction(s)] done [16.46s].
sorting and recoding items ... [608 item(s)] done [0.17s].
creating transaction tree ... done [0.05s].
checking subsets of size 1 2 done [0.07s].
writing ... [0 rule(s)] done [0.00s].
creating S4 object  ... done [0.06s].

Tomamos los mismos parámetros que para el experimento con verdaderas ANK y
no obtuvimos como resutlado ninguna regla. El algoritmo dice que se generaron
608 ítems pero que ninguno cumple con los parámetros que nosotros específicamos
de minsupport o minconfidence.

Recién con estos parámetros obtuvimos algunas reglas (10).

Parameter specification:
 confidence minval smax arem  aval originalSupport maxtime support minlen maxlen target   ext
       0.25    0.1    1 none FALSE            TRUE       5    0.01      2     10  rules FALSE

Algorithmic control:
 filter tree heap memopt load sort verbose
    0.1 TRUE TRUE  FALSE TRUE    2    TRUE

Absolute minimum support count: 380 

set item appearances ...[0 item(s)] done [0.00s].
set transactions ...[159765 item(s), 38051 transaction(s)] done [14.44s].
sorting and recoding items ... [12304 item(s)] done [0.61s].
creating transaction tree ... done [0.08s].
checking subsets of size 1 2 done [15.63s].
writing ... [10 rule(s)] done [0.53s].
creating S4 object  ... done [0.05s].

#### Ensayo 2: MR Modo Bag - Exclusion - Uniform

Parameter specification:
 confidence minval smax arem  aval originalSupport maxtime support minlen maxlen target   ext
        0.9    0.1    1 none FALSE            TRUE       5   0.025      2     10  rules FALSE

Algorithmic control:
 filter tree heap memopt load sort verbose
    0.1 TRUE TRUE  FALSE TRUE    2    TRUE

Absolute minimum support count: 951 

set item appearances ...[0 item(s)] done [0.00s].
set transactions ...[160000 item(s), 38051 transaction(s)] done [15.21s].
sorting and recoding items ... [0 item(s)] done [0.11s].
creating transaction tree ... done [0.01s].
checking subsets of size 1 done [0.00s].
writing ... [0 rule(s)] done [0.00s].
creating S4 object  ... done [0.04s].

Como se puede ver, con los parámetros originales no se obtuvieron reglas de asociación.

Se fueron probando distintas combinaciones de parámetros donde esta fue
la última.

 rules <- apriori(tx, parameter = list(support=0.00446, confidence = 0.0005, minlen = 2))
Apriori

Parameter specification:
 confidence minval smax arem  aval originalSupport maxtime support minlen maxlen target   ext
      5e-04    0.1    1 none FALSE            TRUE       5 0.00446      2     10  rules FALSE

Algorithmic control:
 filter tree heap memopt load sort verbose
    0.1 TRUE TRUE  FALSE TRUE    2    TRUE

Absolute minimum support count: 169 

set item appearances ...[0 item(s)] done [0.00s].
set transactions ...[160000 item(s), 38051 transaction(s)] done [12.76s].
sorting and recoding items ... [7581 item(s)] done [0.15s].
creating transaction tree ... done [0.04s].
checking subsets of size 1 2 done [0.93s].
writing ... [0 rule(s)] done [0.18s].
creating S4 object  ... done [0.06s].

No se obtuvieron reglas de asociación.

#### Ensayo 3: MR Modo Bag - Inclusion - Uniform

Aquí no teníamos un parámetro para tomar de referencia porque no se pudieron generar
transacciones en la iteración anterior.

Parameter specification:
 confidence minval smax arem  aval originalSupport maxtime support minlen maxlen target   ext
        0.9    0.1    1 none FALSE            TRUE       5 0.00035      2     10  rules FALSE

Algorithmic control:
 filter tree heap memopt load sort verbose
    0.1 TRUE TRUE  FALSE TRUE    2    TRUE

Absolute minimum support count: 13 

set item appearances ...[0 item(s)] done [0.00s].
set transactions ...[6508629 item(s), 38051 transaction(s)] done [14.59s].
sorting and recoding items ... [0 item(s)] done [1.14s].
creating transaction tree ... done [0.00s].
checking subsets of size 1 done [0.00s].
writing ... [0 rule(s)] done [0.00s].
creating S4 object  ... done [1.52s].

Con estos parámetros no se obtuvieron reglas de asociación.

#### Ensayo 4: MR Modo Bag - Inclusion - Scrambled

Parámetros originales para Ank Inclusion
-  Min long de MR: 4
-  Min Confidence: 0.80
-  Min Support: 0.0022 (Corte mínimo en 83 apariciones)

Parameter specification:
 confidence minval smax arem  aval originalSupport maxtime support minlen maxlen target   ext
        0.8    0.1    1 none FALSE            TRUE       5  0.0022      2     10  rules FALSE

Algorithmic control:
 filter tree heap memopt load sort verbose
    0.1 TRUE TRUE  FALSE TRUE    2    TRUE

Absolute minimum support count: 83 

set item appearances ...[0 item(s)] done [0.00s].
set transactions ...[7420690 item(s), 38051 transaction(s)] done [14.68s].
sorting and recoding items ... [0 item(s)] done [1.17s].
creating transaction tree ... done [0.00s].
checking subsets of size 1 done [0.00s].
writing ... [0 rule(s)] done [0.00s].
creating S4 object  ... done [1.95s].

Con estos parámetros no se generaron transacciones.

Parameter specification:
 confidence minval smax arem  aval originalSupport maxtime support minlen maxlen target   ext
        0.8    0.1    1 none FALSE            TRUE       5 0.00025      2     10  rules FALSE

Algorithmic control:
 filter tree heap memopt load sort verbose
    0.1 TRUE TRUE  FALSE TRUE    2    TRUE

Absolute minimum support count: 9 

set item appearances ...[0 item(s)] done [0.00s].
set transactions ...[7420690 item(s), 38051 transaction(s)] done [13.91s].
sorting and recoding items ... [332 item(s)] done [1.14s].
creating transaction tree ... done [0.00s].
checking subsets of size 1 2 done [0.00s].
writing ... [0 rule(s)] done [0.00s].
creating S4 object  ... done [1.72s].