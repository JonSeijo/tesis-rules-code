# Encapsula la conexion a sqlite3 para el rule_db_generator.py
# TODO: deberia usarse tambien en el rule_stats de enriquez

import sqlite3

class DBController():
    def __init__(self, db_filename):
        self.filename = db_filename

    def create_connection(self):
        """ Creates a new sqlite file for the database """
        return sqlite3.connect(self.filename)


    def create_tables(self):
        connection = self.create_connection()
        cursor = connection.cursor()

        # Create table 'protein'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS protein
            (idProtein INTEGER PRIMARY KEY,
            family TEXT,
            filename TEXT, 
            encoding TEXT)''')


        # Create table 'rule'
        
        # FIXME: id_rule
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule
            (idRule INTEGER PRIMARY KEY,  
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
            id_rule_metadata INTEGER,
            FOREIGN KEY (id_rule_metadata)
                REFERENCES rule_metadata (id_rule_metadata) 
       )''')


        # 'maximal_repeat_type': ALL, NE, NN ..
        # Create table 'rule_metadata'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule_metadata
            (id_rule_metadata INTEGER PRIMARY KEY,
            rules_filename TEXT UNIQUE,
            family TEXT,
            min_len TEXT,
            transaction_type TEXT,
            maximal_repeat_type TEXT,
            clean_mode TEXT,
            min_support TEXT,
            min_confidence TEXT)''')

        # Create table 'rule_coverage'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule_coverage
            (idRule INTEGER, 
            idProtein INTEGER, 
            fraction REAL, 
            coverageMode INTEGER, 
            consequentOcurrenceType INTEGER, 
            antecedentRepeats TEXT, 
            consequentRepeats TEXT, 
            consequentRepeatsDistances TEXT, 
            consequentAvgRepeatDistance REAL, 
            antecedentRepeatsDistances TEXT, 
            antecedentAvgRepeatDistances TEXT)''')

        # Create table 'item'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item
            (idItem INTEGER, 
            item TEXT, 
            itemFunction INTEGER, 
            qtyRepeats INTEGER, 
            avgDistance REAL, 
            qtyProteins INTEGER)''')

        connection.commit()
        connection.close()


    def insert_rule_coverage_values(self, rule_coverage_values):
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.executemany('''
            INSERT INTO rule_coverage(
                idRule,
                idProtein,
                fraction,
                coverageMode,
                consequentOcurrenceType,
                antecedentRepeats,
                consequentRepeats,
                consequentRepeatsDistances,
                consequentAvgRepeatDistance,
                antecedentRepeatsDistances,
                antecedentAvgRepeatDistances)

            VALUES (
                :idRule,
                :idProtein,
                :fraction,
                :coverageMode,
                :consequentOcurrenceType,
                :antecedentRepeats,
                :consequentRepeats,
                :consequentRepeatsDistances,
                :consequentAvgRepeatDistance,
                :antecedentRepeatsDistances,
                :antecedentAvgRepeatDistances)''', 

            rule_coverage_values)

        connection.commit()
        connection.close()

    def insert_proteins(self, proteins_to_insert):
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.executemany('''
            INSERT INTO protein(idProtein, family, encoding, filename)
            VALUES (:idProtein, :family, :encoding, :filename)''', 
            proteins_to_insert)

        connection.commit()
        connection.close()

    def insert_rule_metadata(self, rule_metadata_to_insert):
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO rule_metadata( 
                rules_filename,
                family,
                min_len,
                transaction_type,
                maximal_repeat_type,
                clean_mode,
                min_support,
                min_confidence)
            VALUES (:rules_filename,
                :family,
                :min_len,
                :transaction_type,
                :maximal_repeat_type,
                :clean_mode,
                :min_support,
                :min_confidence)''',
            rule_metadata_to_insert)

        rule_metadata_last_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return rule_metadata_last_id

    def insert_rules(self, rules_to_insert):
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.executemany('''
            INSERT INTO rule(
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
            VALUES (:rule,
                :antecedent,
                :consequent,
                :rule_type,
                :rule_type_simple,
                :rule_size,
                :count,
                :support,
                :confidence,
                :lift,
                :id_rule_metadata)''', 
            rules_to_insert)

        connection.commit()
        connection.close()

    def insert_items(self, items_to_insert):
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.executemany('''
            INSERT INTO item (idItem, item, itemFunction, qtyRepeats, avgDistance, qtyProteins) 
            VALUES (:idItem, :item, :itemFunction, :qtyRepeats, :avgDistance, :qtyProteins)''', 
            items_to_insert)

        connection.commit()
        connection.close()


    def get_last_protein_id(self):
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT MAX(idProtein) FROM protein")
        id_max_protein = cursor.fetchone()[0]

        connection.commit()
        connection.close()

        return id_max_protein if id_max_protein != None else 0 

    def get_proteins_of_family(self, family):
        connection = self.create_connection()
        cursor = connection.cursor()

        rows = cursor.execute('''
            SELECT idProtein, encoding, filename
            FROM protein
            WHERE family = :family
            ''', [family])

        proteins_of_family = []
        for row in rows:
            proteins_of_family.append({
                'idProtein': row[0],
                'encoding': row[1],
                'filename': row[2],
            })
        

        connection.commit()
        connection.close()

        return proteins_of_family


    def update_rule_coverage(self, rule_coverage_to_update, idRule, idProtein):
        connection = self.create_connection()
        cursor = connection.cursor()

        dict_ids = {
            'idRule': idRule,
            'idProtein': idProtein,
        }

        # Add ids into dict to insert
        rule_coverage_to_update.update(dict_ids)

        cursor.execute('''
            UPDATE rule_coverage 
            SET consequentOcurrenceType = :consequentOcurrenceType, 
                antecedentRepeats = :antecedentRepeats,
                consequentRepeats = :consequentRepeats,
                consequentRepeatsDistances = :consequentRepeatsDistances,
                consequentAvgRepeatDistance = :consequentAvgRepeatDistance,
                antecedentRepeatsDistances = :antecedentRepeatsDistances,
                antecedentAvgRepeatDistances = :antecedentAvgRepeatDistances
            WHERE idRule = :idRule AND idProtein = :idProtein
            ''', 
            rule_coverage_to_update)

        connection.commit()
        connection.close()

    """ 
    Returns an iterable to the rule coverage table joined with the relevant fields 
    in order to query the stat for rules/items 
    """
    def get_rule_coverage_iterator(self):
        connection = self.create_connection()
        cursor = connection.cursor()
        res = cursor.execute('''
            SELECT rc.idRule, rc.idProtein, p.encoding as protein, r.rule as rule FROM rule_coverage rc
            INNER JOIN protein p on p.idProtein = rc.idProtein
            INNER JOIN rule r on r.idRule = rc.idRule
            ''')

        rule_coverages = [{
            'idRule': row[0],
            'idProtein': row[1],
            'protein': row[2],
            'ruleStr': row[3]
            } for row in res
        ]

        connection.commit()
        connection.close()

        return rule_coverages

    def get_rules(self):
        connection = self.create_connection()
        cursor = connection.cursor()

        res = cursor.execute('''SELECT idRule, rule FROM rule''')
        rules = [{
                'idRule': row[0],
                'rule': row[1]
            } for row in res]

        connection.commit()
        connection.close()

        return rules

