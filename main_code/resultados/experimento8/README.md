## Experimento 8 - Más detalles de coberturas de proteínas por reglas

### Base de coberturas

Se generaron dos bases de datos SQLite donde se guardan las reglas computadas, las proteínas analizadas y las ocurrencias de dichas reglas en las proteínas mencionadas, almacenando también el fracción de cobertura y el modo (qué parte la regla está afectada, consecuente, antecedente o ambas).

En un primer approach se guardaron aquellas ocurrencias cuya fracción de cobertura fuera positiva, es decir, que existiera al menos alguna ocurrencia de algún ítem de la regla en la proteína y se marcó además que parte de la regla ocurría (coverageMode).

En una segunda iteración sobre esto se decidió hacer más estricto este criterio y marcar solo aquellas reglas cuyos integrantes estuvieran completamente en las proteínas: todos los antecedentes y el consecuente con ocurrencias en las proteína en cuestión. Esto por supuesto arroja un número mucho menor de ocurrencias.

Una de las preguntas que surgieron era *Ver qué reglas y en cuáles proteínas, hay antecedentes que aparezcan pero no así los consecuentes de estas reglas.*. Para esto sirve tener la primera base de datos en la que se puede ver mejor las ocurrencias parciales de reglas en proteínas.

#### Consultas realizadas a la base

Se generaron dos listados:
- Las proteínas que no son cubiertas por ninguna regla: son más de 12k de proteínas que no tienen ninguna cobertura por reglas.
- Listado de reglas que cubren a **ikba**. Hay 81 reglas que cubren a esta proteína. De aquí se ve algo más: hay muchas reglas que parecen estar contenidas en otras, como por ejemplo:
    - {ALHL,PLHL,TALH} => {LHLA} en {ALHL,PLHL,TALH,TPLH} => {LHLA}

Del grupo que no eran cubiertos por nada lo que se observó fue que en promedio parecían proteínas más cortas (ver los análisis resumen-*.txt). Se tomaron las +12k proteínas y se corrió un pequeño programa para analizar la distribución de aminoácidos y la longitud de las proteínas (media, mediana y desvío). Lo único que se observó fue una diferencia de longitud de este grupo respecto de tres grupos similares (12k proteínas cada uno tomadas al azar del grupo de proteínas ANK).


#### Reglas interesantes

GADV, PLHL -> LHLA (acá vimos como se marcan los motivos de la proteina en uniprot)