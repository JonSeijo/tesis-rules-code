"""
Convertí el script que genera la db para que use multiprocess en la parte intensa.
Este script es para leer ambas dbs y ver si tiene diferencias

https://stackoverflow.com/questions/46867476/comparing-two-sqlite-databases-using-python
"""

import sqlite3

db1 = "protein-rules-singlethread.db"
db2 = "protein-rules-multithread.db"

tblCmp = "SELECT * FROM rule_coverage"

conn1 = sqlite3.connect(db1)
conn2 = sqlite3.connect(db2)

cursor1 = conn1.cursor()
result1 = cursor1.execute(tblCmp)
res1 = result1.fetchall()

cursor2 = conn2.cursor()
result2 = cursor2.execute(tblCmp)
res2 = result2.fetchall()

res1 = set(res1)
res2 = set(res2)
result = res1.symmetric_difference(res2)

print("Diferencias entre single y multithread:")
print(result)