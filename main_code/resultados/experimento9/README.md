# Experimento 9 - Clausura de reglas

En esta ocasión lo que se hizo fue tomar el conjunto de reglas y analizar si estás estaban conectadas, es decir, si estas formaban grupos o particiones basado en la relación entre reglas que cubren a proteínas.

Para esto se calculó la clausura transitiva del conjunto de reglas. Tomamos una regla y a partir de ella se vio qué proteínas eran cubiertas por dicha regla.

Una vez que obtenidas estas proteínas, se calcularon que nuevas reglas aplicaban para estas proteínas y se las agregó al mismo grupo.

Esto se repite para cada hasta que no podamos agregar reglas al grupo actual. Si no hay más reglas disponibles, el proceso termina. Si las hay, se repite el proceso y se arma otro grupo.

En este caso, la clausura transitiva de las proteínas arrojó un solo grupo con todas las reglas en él.

Se invoca al programa `rule_closure` pasando como parámetro el archivo SQLite donde está la base de datos con reglas, proteínas y coberturas.

```bash
python3 rule_closure.py --filename=protein-rules.db
```