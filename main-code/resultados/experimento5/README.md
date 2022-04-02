# Experimento 5

Se tomaron todas reglas ordenadas por _lift_ del archivo del *Experimento 2* mr-bag/rules-ank-mr-bag-4-exclusion.csv y
se hizo el camino inverso, es decir, para cada regla tratar de matchear aquellas proteínas que contengan todos los ítems de la regla en cuestión.

```bash
./rule_parse_app resultados/experimento5-toda/rulefile.txt ../../data/proteins/familyDataset/ank/ resultados/experimento5
```

Además con el programa actual se generaron qué proteínas matcheaban con qué reglas y se generaron los contextos de los consecuentes para entender qué los rodea.

Utilizando esta información se generaron logos de alineamientos utilizando:


```bash
sh generatelogos.sh
```

que a través del ```skylign-client``` y via API generan los logos a partir de la carpeta alineamientos/ y los .sto que están allí.