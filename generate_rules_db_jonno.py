# TODO: Mergear con rule_db_generator.py 

import sqlite3

filename_db = "output/dbs/rules_db_jonno.db"

def create_tables(connection):
    print("Creating tables...")

    cursor = connection.cursor()

    # TODO: Mergear. Esto es igual a la tabla ya existente.
    #   solo habria que expandirla con los nuevos fields
    
     # 'ruleTypeDelta': Ej, si es +1/+2 agrega 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rule_jonno
        (id_rule INTEGER PRIMARY KEY,
        rule TEXT,
        antecedent TEXT,
        consequent TEXT,
        rule_type INTEGER,
        rule_type_delta INTEGER,
        rule_filename TEXT,
        support REAL,
        confidence REAL,
        lift REAL,
        id_rule_metadata INTEGER)''')

    # 'maximalRepeatType': ALL, NE, NN ..
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rule_metadata
        (id_rule_metadata INTEGER PRIMARY KEY,
        rules_filename TEXT,
        family TEXT,
        min_support TEXT,
        min_confidence TEXT,
        min_len TEXT,
        maximal_repeat_type TEXT)''')

    connection.commit()

if __name__ == '__main__':

    print("Connecting to db:", filename_db)
    connection = sqlite3.connect(filename_db)

    create_tables(connection)

    connection.close()
