## Experimento 7 - Agrupamiento y coverage de reglas

Se toman 394 reglas de MBA para la familia ANK (38k proteínas) con el criterio de 
cálculo de MRs como bolsa y limpiando aquellos MRs más extensos (exclusión).

### Agrupamiento

Luego de analizar las reglas calculadas, vimos que podíamos agruparlas básicamente 
en tres grupos.

- Aquellas en donde el consecuente era un *overlapping* de los antecedentes por ejemplo:
 `{LISH},{SHGA} => {ISHG}`
- Aquellas en donde el consecuente *agregaba* información, es decir, aportaba algún 
aminoácido que no aparecía en los antecedentes, por ejemplo: 
 `{AGAD,LEAG} => {LLEA}`
- El resto de las reglas que no tenían un comportamiento descripto por los dos incisos
anteriores, por ejemplo: 
`{LHLA,PLHI} => {LHIA}`

En el archivo *Experimento #7 > Reglas Agrupadas* se puede ver un excel con el resultado de la clasificación antes propuesta.

En la mayoría de los casos se puede ver que son reglas del estilo overlapping. Mientras que una particularidad de las "agrega" es que está repartido entre tres aminoácidos **A**, **T** y **L**. Solo hay uno que agrega **TP** al grupo.

### Cobertura

Por un lado se vieron las coberturas de las distintas reglas. Queríamos ver qué tan relevantes son sus partes integrantes dentro del conjunto de proteínas estudiadas. Tomamos las 394 reglas que obtuvimos para la bolsa de MR en las que quitamos las ocurrencias de los MRs que eran superconjuntos de los que conservamos.

Se generaron tres visualizaciones, un excel con tres columnas con el nombre del archivo, el porcentaje de cobertura y el encoding de la proteína. Una imagen donde se ve con colores gráficamente las posiciones de la proteína cubierta. Y por último, un html que también marca con colores (antecedente, consecuente o ambos) la ocurrencia de alguna regla en la proteína pero más detallado que la imagen.

Se compararon las reglas evaluando la cobertura entre las familias ANK, ANK-Scrambled y ANK-Uniform.

##### ANK

    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
    0.00000 0.02326 0.04679 0.06344 0.08767 0.51652 

##### ANK-Scrambled

    Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
    0.000000 0.000000 0.005038 0.007703 0.011679 0.141509 

##### ANK-Uniform

    Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
    0.000000 0.000000 0.000000 0.002357 0.003031 0.166667 

Se generaron un par de gráficos para comparar el rendimiento de las tres familias analizadas.

También se calcularon tres tandas de visualizaciones HTML y PNG para ANK y también se vio el detalle de ikba. 

Las visualizaciones condensan en una proteína todas las ocurrencias de las reglas por lo cual, podría haber reglas que no aplican a la proteína (aplican en el sentido que aparezcan todos sus componentes en la regla en cuestión) que 
pinten la zona de la proteína pero en realidad no tengan sentido.

Esto se volverá a tomar en otro experimento usando las reglas que aplican solamente.

### Otros

Se generaron otros logos para analizar con 
http://weblogo.threeplusone.com/