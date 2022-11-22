# Experimento 13 - Distancias de ocurrecias consecutivas con reglas clusterizadas

Repetimos el experimento 12 donde analizamos las distancias de los consecuentes
pero considerando a las reglas de forma clusterizada.

Para clusterizar las reglas lo que se hizo fue continuar con el concepto de sinónimos
a partir de la distancia de edición como se definió para el experimento anterior.

Esta variante es, sin embargo, una versión más relajada del caso anterior. 
Por ejemplo, si tenemos una regla A1, B1 -> C1. Y sean A2, B2, C3, sinónimos
de A1, B1, y C1 respectivamente.

Decimos que la proteína está cubierta por la regla si están presentes sus
antecedentes y el consecuente. Para el caso de la regla de clusterizada,
diremos que cubre a una proteína si el consecuente o sus sinónimos están presentes
y además, los antecedentes o sus sinónimos están presentes.

Volvamos al ejemplo anterior, si: A1, B1 -> C1 es la regla y tenemos el 
siguiente agrupamiento de items de acuerdo a sus sinónimos:
{A1, A2}, {B1, B2} y {C1, C2}, entonces la siguiente proteina
"xxxxA2xxxB1xxxxxC2xxx" va a estar cubierta por la regla mencionada.

```bash
python3 rule_stats.py --filename="../resultados/experimento10/protein-rules-test.db" --mode="cluster-distances"
```

Se generan muchos más registros para este caso. Se corren los mismos gráficos
que para los experimentos anteriores.

### TODO: Hacer análisis de los gráficos.