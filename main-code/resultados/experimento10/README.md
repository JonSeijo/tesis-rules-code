# Experimento 10 - Estadísticas sobre reglas e ítems

En este experimento Se realizaron dos pruebas. Por un lado se tomó todo el conjunto de reglas y se tomaron los ítems que las componen, es decir, se armó una lista con todas los tetrámeros que están presentes en las reglas.

### Frecuencias de ítems en proteínas vs. en reglas

Luego se calculó para cada uno de estos cuál es su frecuencia de aparición tanto en el conjunto de reglas como en todo el conjunto de las proteínas que dieron origen a esas reglas y se compararon con la idea de establecer si la frecuencia de los ítems en las reglas viene dada por la frecuencia propia de esos ítems en el conjunto de proteínas o si responde a otro fenómeno.

```bash
python3 rule_stats.py --filename=protein-rules.db --mode="add-stats"
```

### Info estadística en coberturas e ítems

En otro ensayo se analizó la tabla de coberturas de reglas y proteínas, y se calcularon nuevos estadísticos. Tanto para antecedentes como para consecuentes se analizó donde se repiten en la proteína, las distancias entre repticiones consecutivas y la distancia promedio de repeticiones (si corresponde).
Además, se clasificó la ocurrencia del consecuente entre tres opciones: si ocurre aislado, si el consecuente ocurre aislado, solapado con algún antecedente o si la ocurrencia es mixta, es decir, que ocurre en ambas configuraciones para una misma proteína.

```bash
python3 rule_stats.py --filename=protein-rules.db --mode="coverage-stats"
```


También se agregó a la base de datos información estadística sobre los ítems que componen cada una de las reglas. Tomamos todos los ítems únicos de todas las reglas y se cálculo cuál es la función de cada ítem (si es un consecuente o un antecedente según corresponda), la cantidad de repeticiones del ítem en las proteínas, la cantidad de proteínas únicas en las que el ítem aparece y la distancia promedio entre repeticiones del ítem si es que corresponde respecto del conjunto total de proteínas.

```bash
python3 rule_stats.py --filename=protein-rules.db --mode="freq"
```

(Notar que los dos primeras invocaciones del programa en este archivo han quedado deprecadas de acuerdo al refactoring que se hizo del programa rule_stats y que se pasaron al rule_db_generator)