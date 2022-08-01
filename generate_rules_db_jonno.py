# TODO: Mergear con rule_db_generator.py 

import sqlite3

import info_rules

filename_db = "output/dbs/rules_db_jonno.db"

def delete_tables(connection):
    print("- Deleting old tables...")
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE rule_jonno''')
    cursor.execute('''DROP TABLE rule_metadata''')
    connection.commit()


def create_tables(connection):
    print("- Creating new tables...")

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
        rule_type TEXT,
        rule_type_simple TEXT,
        rule_size INTEGER,
        count INTEGER,
        support REAL,
        confidence REAL,
        lift REAL,
        id_rule_metadata INTEGER)''')

    # 'maximalRepeatType': ALL, NE, NN ..
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rule_metadata
        (id_rule_metadata INTEGER PRIMARY KEY,
        rules_filename TEXT UNIQUE,
        family TEXT,
        min_support TEXT,
        min_confidence TEXT,
        min_len TEXT,
        maximal_repeat_type TEXT)''')

    connection.commit()

def insert_rule_metadata(connection, family, min_len, 
        mr_type, min_support, min_confidence, filename_rules):
    
    print("- Inserting rules metadata")
    
    rule_metadata = (filename_rules, family, 
        min_support, min_confidence, min_len, mr_type)
    
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO rule_metadata( 
            rules_filename,
            family,
            min_support,
            min_confidence,
            min_len,
            maximal_repeat_type)
        VALUES (?,?,?,?,?,?)''', rule_metadata)

    rule_metadata_id = cursor.lastrowid
    
    connection.commit()

    return rule_metadata_id

# Podria haber usado algo como pandas.DataFrame.to_sql? Si
def insert_rules(connection, rules_df, metadata_id):
    print("- Inserting rules data")
    cursor = connection.cursor()

    for index, rr in rules_df.iterrows():

        rule_to_insert = (
            rr['rules'],
            rr['antecedent'],
            rr['consequent'],
            rr['ruletype'],
            rr['ruletype_simple'],
            rr['rule_size'],
            rr['count'],
            rr['support'],
            rr['confidence'],
            rr['lift'],
            metadata_id
        )

        cursor.execute('''
            INSERT INTO rule_jonno(
                rule,
                antecedent,
                consequent,
                rule_type,
                rule_type_simple,
                rule_size,
                count,
                support,
                confidence,
                lift,
                id_rule_metadata)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', rule_to_insert)

    connection.commit()


if __name__ == '__main__':

    # TODO: Parametrizar
    # TODO: Permitir pasar directamente un rule path?
    family = "NEWAnk"
    min_len = "len4"
    mr_type = "ALL_sub"
    min_support = "0.025"
    min_confidence = "0.9"

    filename_rules = f"output/rules/{family}_{min_len}_{mr_type}_s{min_support}_c{min_confidence}.csv"
    # filename_rules = "output/rules/NEWAnk_len4_ALL_sub_s0.025_c0.9.csv"

    print("\n\n\n\n")
    print("filename_rules:", filename_rules)


    print("Connecting to db:", filename_db)
    connection = sqlite3.connect(filename_db)

    # TODO: parametrizar flush
    delete_tables(connection)

    create_tables(connection)

    rules_df = info_rules.build_df_rules_from_path(filename_rules)
    
    metadata_id = insert_rule_metadata(connection, family, min_len, 
        mr_type, min_support, min_confidence, filename_rules)

    insert_rules(connection, rules_df, metadata_id)

    connection.close()
