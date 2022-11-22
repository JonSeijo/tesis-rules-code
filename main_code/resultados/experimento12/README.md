# Experimento 12 - Revisión de frecuencias y distancias con agrupamientos

Revisión de experimentos 10 y 11 repitiendo alguno de estos ensayos pero 
agrupando por distancias considerando el grafo de distancias de edición 
según la métrica de Levenshtein.

Se implementó el cálculo de distancias según la fórmula de Levenshtein 
en el archivo ```metrics.py```. Además se calculó el grafo según las 
distancias menores a cierta cota y se lo graficó haciendo:

```bash
python3 rule_stats.py --filename="../resultados/experimento10/protein-rules-test.db" --mode="graph-distances" --edt=2
```

Esto nos generó un archivo PNG con el detalle del grafo que relaciona ítems 
con sus distancias de edición entre sí.

A partir de las componentes conexas de este grafo se tomó un representante de 
cada una de ellas y se estableció el concepto de sinónimos. Decimos que dos 
ítems son sinónimos si su distancia de edición entre sí es menor que cierto 
valor. Gráficamente, son sinónimos si están dentro del mismo bosque en el 
grafo de distancias de edición.

A continuación se repiten los experimentos de frecuencias de ítems 
agrupados por las distancias de edición

```bash
python3 rule_stats.py --filename="../resultados/experimento10/protein-rules-test.db" --mode="freq" --ged=1
```

## Distancias

Repetimos el experimento de las distancias consecutivas entre ítems para los consecuentes.

```bash
python3 rule_stats.py --filename="../resultados/experimento10/protein-rules-test.db" --mode="distances"
```

Luego, considerando sinónimos para los consecuentes de acuerdo a como definimos antes
los agrupamientos según la distancia de edición. Surgen dos criterios para considerar
a la hora de computar las distancias consecutivas:

- *(Modo 1)* Por un lado, la presencia de todos los sinónimos de un consecuente a la hora 
de calcular la distancia de repeticiones consecutivas. 
Por ej, Si tenemos que A,B -> C y (C1 es sinónimo de C), tomar la distancia consecutiva entre las
ocurrencias de C y C1.

```bash
python3 rule_stats.py --filename="../resultados/experimento10/protein-rules-test.db" --mode="distances" --ged=1 --groupingmode=1
```

- *(Modo 2)* Similar al anterior pero solo si existe C1 como consecuente de una regla y sus antecedentes 
están presentes en la proteína. Ej., si A1,B1 -> C1 chequear que antes existan A1 y B1 para
considerar C1 como una repetición válida.

```bash
python3 rule_stats.py --filename="../resultados/experimento10/protein-rules-test.db" --mode="distances" --ged=1 --groupingmode=2
```

Después de generar estos datos los guardamos en carpetas separadas según agrupado o no
y considerando el modo de agrupamiento empleado.

Con los datos de frecuencias de ítems y proteínas, los graficamos en forma conjunta
para tratar de determinar si había alguna relación entre la frecuencia de aparición
de ciertos ítems en las reglas. Vimos que había ítems que aparecían más frecuentemente
que otros por lo que nos planteamos la pregunta de si estos ítems en realidad son
más preponderantes en las reglas porque son más frecuentes, a su vez, en las proteínas.

A priori no encontramos una relación directa entre las frecuencias de aparición 
en proteínas y reglas por lo cual sospechamos que esta distribución de ítems
en reglas no se deba solamente a un fenómeno de ser 4-méros comunes en las proteínas.

También analizamos como estaban distribuidas las distancias entre las repeticiones
consecutivas de los consecuentes de las reglas que tenemos.

Graficamos para esto la distribución según tipo de consecuente (de acuerdo a como
ocurren en la proteína: Overlapped, Isolated & Mixed). También la frecuencias
según tipo de ítems para los más frecuentes (gráficos de densidad y boxplots).