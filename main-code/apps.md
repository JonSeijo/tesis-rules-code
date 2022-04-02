# Programas

## C++

Programa | Función | Entrada | Salida
--- | --- | --- | ---
freq_dist (calculate_freq_dist_for_family.cpp) | Calcula al frecuencia de distribución de los aminoácidos para una familia de proteínas. | Directorio donde están las proteínas | un .txt con la frecuencia de los aminoácidos parseados
cleaner (cleaner.cpp) | Limpia los archivos de transacciones dependiendo del modo (substring o superstring) | input (archivo a limpiar), mode (modo de operación: super o substring) y out (archivo de salida) | Archivo con las tx limpias
coverage (compute_coverage_family.cpp) | Usado para reproducir los resultados del paper de Pablo. Calcula la cobertura los mrs para ikba según la longitud de los mrs | Path de donde tomar las proteínas | Archivo con datos de cobertura según la longitud del MR
db (create_db.cpp) | Genera una base de datos sqlite con los datos de MRs y proteínas de una familia | Path a la carpeta con los fastas de las proteínas y nombre o identificador de la familia en cuestión | Genera un archivo sqlite con los datos de MRs y proteínasp para la familia recibida como parámtero
txmba_orig (create_tx_for_mba.cpp) | (deprecado) Crea archivos con transacciones a partir de leer proteínas de una carpeta. Cada transacción tiene (MRi, MRi+1, ..., MRi+k, IDFamilia). MRs se calculan para cada proteína | path (de donde tomar las proteínas) familyName (identificador de la familia) minLength (mínima longitud de MR a considerar) minOcurrences (cantidad mínima de ocurrencias del MR en la proteína para considerar) | Archivo con las transacciones creadas.
rule_parse_app (rule_parse_app.cpp) | Genera a partir de reglas y proteínas los archivos de alineamiento para graficar las ocurrencias de reglas en contextos de proteínas y hace el backwards match a partir de una regla, que proteínas aplican para esa regla | ruleFile (donde están las reglas MBA) proteinDirectory (el directorio de proteínas a donde corresponden esas reglas) outDirectory (directorio de salida para los archivos de alineamiento)  | Archivos de alineamiento
scrambler_app (scrambler_app.cpp) | A partir de un directorio de proteínas genera las variaciones (scrambled o uniform según sea el caso) de las proteínas recibidas como parámetro respetando cantidad de proteínas original y largo de las mismas | input (directorio de las proteínas a modificar) output (directorio donde guardar las proteínas modificadas) mode (si genera variaciones uniformes de acuerdo al input o si a partir del input desordena los valores presentes) | Genera los archivos correspondientes a las variaciones solicitadas en el directorio pedido con las mismas características del original.
txmba_bag (txmba_bag.cpp) | Genera transacciones a partir de proteínas en el modo bag, es decir, concatena todas, les calcula los MRs y luego por cada una las escribe en el archivo de salida | path (de donde tomar las proteínas) familyName (identificador de la familia) minLength (mínima longitud de MR a considerar) minOcurrences (cantidad mínima de ocurrencias del MR en la proteína para considerar) | Archivo de txs generadas
txmba_each (txmba_each.cpp) | Crea archivos con transacciones a partir de leer proteínas de una carpeta. Cada transacción tiene (MRi, MRi+1, ..., MRi+k, IDFamilia). MRs se calculan para cada proteína | path (de donde tomar las proteínas) familyName (identificador de la familia) minLength (mínima longitud de MR a considerar) minOcurrences (cantidad mínima de ocurrencias del MR en la proteína para considerar) | Archivo con las transacciones creadas.

## Python 3

Programa | Función | Entrada | Salida
--- | --- | --- | ---
fastaread.py | Utilidades para leer archivos fasta y ver proteínas. Se puede usar como una biblioteca o como invocarlo con argumentos | inputFile (un archivo fasta para leer) | Los datos parseados
graph.py | Genera un grafo de implicaciones entre consecuentes y antecedentes en función de las reglas. Además gráfica la frecuencia de aparición en las proteínas y opcionalmente resalta ikba. | ruleFile (el archivo con las reglas generadas a parsear) proteinPath (el path donde están las proteínas) threshold (la cantidad mínima de ejes salientes a considerar para incluir en el gráfico) highlightIkba (si destacar donde interviene la proteína de referencia) | Genera un png con el grafo de implicaciones
protein_stats.py | A partir de una lista de proteínas calcula estadísticos para longitudes y calcula la frecuencia de distribución de los aminoácidos presentes en ella | proteinPath (la ruta de donde tomar las proteínas) proteinFile (lista de proteínas a analizar) | Muestra los datos calculados por pantalla
rule_closure.py | Calcula la clausura transitiva de un grupo de reglas en proteínas que lee de una BBDD SQLite. Escribe los grupos en los que queda divida la clausura en un archivo | filename (nombre del archivo sqlite a leer, se asume que está en el formato usado a lo largo del trabajo) | output.txt donde están los grupos generados luego del cómputo de la clausura.
rule_db_generator.py | Genera una BBDD SQLite con las reglas, proteínas y la información de cobertura de proteínas por reglas | proteinPath (la ruta de donde tomar las proteínas) ruleFile (el archivo que contiene las reglas generadas) add (si agregar o no proteínas a la base de datos) filename (nombre del archivo sqlite) | Las proteínas cargadas en la base.
rule_stats.py | Computa estadísticas para la base de reglas que se tiene: calcula frecuencias de ítems en reglas y en la base, computa distancias entre repticiones consecutivas. Genera grafos de ítems de acuerdo a como se relacionan. Genera análisis de distancias pero también para reglas clusterizadas. Grafica matriz de co-ocurrencia de items entre sí según donde ocurren. | filename (el nombre del archivo de la base de datos) mode (modo de operación, si agrega info de cobertura, de ítems o frecuencias de ocurrencia de ítems en proteínas vs reglas) edt (umbral de distancia de edición mínima a considerar) ged (si agrupar o no por distancia de edición) groupingmode (modo de agrupamiento (en el caso de agrupar por distancias)) | Varía según el modo que se llame al programa.
rule_coverage.py | Parsea un archivo de reglas y otro de proteínas y calcula como esas reglas cubren el conjunto de proteína. Además permite exportar en diversos formatos estos resultados (vector, imagen, csv, html, etc) | proteinFile (el archivo de proteínas a analizar) ruleFile (el archivo de reglas a analizar) coverageFile (donde hacer la salida del resultado de cobertura) exportType (el modo de exportar los datos) onlyCovered (si solo considerar proteínas que tienen cobertura y descartar aquellas que no son cubiertas por nada) | El resultado de la cobertura dependiendo del archivo y el modo deseado de exportar los datos
rulecoveragebyruletype.py | Similar a rule_coverage solo que distingue según los tipos de reglas definidos | proteinFile (el archivo de proteínas a analizar) ruleFile (el archivo de reglas a analizar) coverageFile (donde hacer la salida del resultado de cobertura) exportType (el modo de exportar los datos) onlyCovered (si solo considerar proteínas que tienen cobertura y descartar aquellas que no son cubiertas por nada) | El resultado de la cobertura dependiendo del archivo y el modo deseado de exportar los datos
rulegroup.py | Lee una archivo de reglas y de acuerdo a los criterios que se elaboraron de clasificación de reglas, clasifica cada una de las reglas | inputFile (el archivo de donde tomar las reglas a agrupar) outputFile (el archivo donde dejar los resultados de la clasificación) | El archivo con los resultados de la clasificación de reglas
logo_maker.py | Permite crear un logo con frecuencias a partir de un archivo .sto | inputFile (el archivo de donde leer los datos del logo.) | Un archivo html con un svg armado de acuerdo a las frecuencias observadas

## Otras bibliotecas

- protein.cpp:
    - parsear proteínas
    - agrupamiento y estadísticas de aminoácidos
- parse.cpp:
    - lectura de archivos fasta
    - invocación de programa externo para el cálculo de MRs
    - cálculo de la función m()
    - cálculo de cobertura y familiaridad (paper de Pablo)
- rulecoverageexport.py:
    - implementación de distintas formas de exportar la cobertura de reglas para proteínas
- filesampler.py:
    - generar muestras de archivos a partir de los contenidos de una carpeta
