## Experimento 1

Se computaron los MRs para 38000 proteínas de la familia _Ankyrin_ en dos tandas. Aquellos
de longitud mayor o igual a 4 y aquellos de longitud mayor o igual a 6 a través del ejecutable `txmba` 

Con esto se armaron _transacciones_, es decir, para cada proteína tomamos los MRs que estuvieran presentes
en estas y generamos items para poder alimentar el algoritmo de generación de reglas de negocio
para utilizar la técnica de _Market Basket Analysis_.

```bash
./txmba ./cosas-tesis-escritorio/data/proteins/familyDataset/ank/ - 4 1 38000 ank-mr4.txt
```

### Ensayo 1
-  Min long de MR: 6
-  Min Confidence: 0.8
-  Min Support: 0.006
-  De 38000 proteínas se obtienen 13654 transacciones. 
Y con estos parámetros obtenemos 1681 reglas de asociación

### Ensayo 2
-  Min long de MR: 4
-  Min Confidence: 0.9
-  Min Support: 0.0040
-  De 38000 proteínas se obtienen 32778 transacciones. 
Y con estos parámetros obtenemos 3279 reglas de asociación

### Caveat

Notar que aquí se computaron (a diferencia del experimento 2) los MRs no de toda la bolsa de 
proteínas sino proteina a proteína.

El modo *bag* consiste en concatenar todas las proteínas en un mismo string y a estos tomarle los maximal repeats.