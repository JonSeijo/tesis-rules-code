#include <iostream>
#include <string>
#include "sqlite3.h"
#include <boost/filesystem.hpp>
#include "parse.h"
#include <boost/algorithm/string/join.hpp>
 // or <experimental/filesystem> in new compilers
 
namespace fs = boost::filesystem;

using namespace std;

/**
 * Runs a SQL statement against a DB instance. It checks for error if the command fails.
 * @param const char* sql the sql statement to run
 * @param sqlite3 db the pointer to the DB
 */
void runStatement(const char* sql, sqlite3* db)
{
    char* error;
    int res;

    /* Execute SQL statement */
    res = sqlite3_exec(db, sql, NULL, 0, &error);
    if (res != SQLITE_OK) {
        cout << "Error with SQL command: " << error << endl;
        sqlite3_free(error);
    }
}

/**
 * Creates the tables for storing the data. Creates a protein and a mr table
 * @param sqlite3 db the pointer to the DB
 */
void createTables(sqlite3* db)
{
    char* sql;

    /* Create SQL statement */
    sql = "CREATE TABLE protein ("
     "`idProtein` INTEGER PRIMARY KEY AUTOINCREMENT, "
     "`filename` CHAR(128) NOT NULL, "
     "`comment` CHAR(255), "
     "`family` CHAR(50), "
     "`protein` TEXT NOT NULL); "
     
     "CREATE TABLE mr ("
     "`idMr` INTEGER PRIMARY KEY AUTOINCREMENT, "
     "`mr` CHAR(100), "
     "`length` INT NOT NULL, "
     "`proteinId` INT NOT NULL, "
     "`qtyOcurrences` INT NOT NULL, "
     "`ocurrences` TEXT);";
    
    runStatement(sql, db);
}

/**
 * Creates indexes for speeding up queries to the DB
 * @param sqlite3 db the pointer to the DB
 */
void createIndexes(sqlite3* db)
{
    char* sql = "CREATE INDEX idx_mr_len ON mr (length);"
     "CREATE INDEX idx_mr_protein_id ON mr (proteinId);"
     "CREATE INDEX idx_protein_family ON protein (family);";

    runStatement(sql, db);
}

/**
 * Escape sql strings
 * @param  string s the string to quote
 * @return string the escaped and correctly quoted string
 */
string quotesql( const string& s )
{
    return string("'") + s + string("'");
}

/**
 * Inserts proteins into the DB
 * @param sqlite3_stmt* stmt  the insertion statement for protein table
 * @param string protein  the protein to be inserted
 * @param string filename the filename of the protein
 * @param string comment  the file comment in the fasta file
 * @param string family   and identification for the protein's family
 */
void insertProtein(sqlite3_stmt* stmt, string protein, string filename, string comment, string family)
{
    sqlite3_bind_text(stmt, 1, filename.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, comment.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 3, family.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 4, protein.c_str(), -1, SQLITE_TRANSIENT);

    sqlite3_step(stmt);
    sqlite3_clear_bindings(stmt);
    sqlite3_reset(stmt);
}

/**
 * Inserts mr data into the DB
 * @param sqlite3_stmt* stmt  the insertion statement for MR data
 * @param string length  the lenght of the mr
 * @param string proteinId the id of the related protein
 * @param string ocurrences ocurrences of the mr in the protein
 * @param string mr    the mr itself
 * @param string qtyOcurrences   the amount of ocurrences of the mr in the protein
 */
void insertMrData(sqlite3_stmt* stmt, string length, string proteinId, string ocurrences, string mr, string qtyOcurrences)
{
    sqlite3_bind_text(stmt, 1, mr.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, ocurrences.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 3, length.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 4, proteinId.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 5, qtyOcurrences.c_str(), -1, SQLITE_TRANSIENT);

    sqlite3_step(stmt);
    sqlite3_clear_bindings(stmt);
    sqlite3_reset(stmt);
}


static int proteinSelectCb(void *data, int argc, char **argv, char **azColName)
{
   string* p = static_cast<string*>(data);
   *p = string(argv[0]);

   return 0;
}

/**
 * Returns the protein id from the DB
 * @param  sqlite3* db the pointer to the db instance
 * @param  string protein the protein to search for its id
 * @return string the protein id
 */
string getProteinId(sqlite3* db, string protein)
{
    char* error;
    string proteinId;
    string sql = "SELECT idProtein FROM protein WHERE protein LIKE '\%"+ protein + "\%'";
    
    if (sqlite3_exec(db, sql.c_str(), proteinSelectCb, &proteinId, &error) != SQLITE_OK) {
        cout << "Error with SQL command: " << error << endl;
        sqlite3_free(error);
    }

    return proteinId;
}



int main(int argc, char* argv[])
{
    char* error;
    sqlite3* db;
    int res;

    if (argc < 3) {
        cout << "Usage: " << argv[0] << " path familyName" << endl;
        return 1;
    }
 
    
    fs::path p(argv[1]);
    if(!exists(p) || !is_directory(p)) {
        std::cout << p << " is not a path\n";
        return 1;
    }


    string familyName = string(argv[2]);
    sqlite3_initialize();
    
    /* Open database */
    res = sqlite3_open("test.db", &db);
    if (res) {
      cout << "Database failed to open: " << sqlite3_errmsg(db) << endl;
    } 

    //Create tables
    createTables(db);
    
    sqlite3_exec(db, "BEGIN TRANSACTION", NULL, NULL, &error);
    sqlite3_exec(db, "PRAGMA synchronous = OFF", NULL, NULL, &error);
    sqlite3_exec(db, "PRAGMA journal_mode = OFF", NULL, NULL, &error);
    sqlite3_exec(db, "PRAGMA temp_store = MEMORY", NULL, NULL, &error);
    sqlite3_exec(db, "PRAGMA page_size = 16384", NULL, NULL, &error);
    sqlite3_exec(db, "PRAGMA cache_size = 16384", NULL, NULL, &error);
    
    //Search for proteins, and insert them
    fs::recursive_directory_iterator begin(p), end;
    std::vector<fs::directory_entry> files(begin, end);
    //std::vector<string> v(files.size(), ""); //Maybe optimal
    
    int pushed = 0;
    int records = 0;
    clock_t cStartClock = clock();

    //Prepare insert statement for proteins
    sqlite3_stmt * proteinStatement;
    string proteinSql = "INSERT INTO protein (filename, comment, family, protein) VALUES (@filename, @comment, @family, @protein)";
    sqlite3_prepare_v2(db, proteinSql.c_str(), 512, &proteinStatement, NULL);

    //Prepare insert statement for mrs
    sqlite3_stmt * mrStatement;
    string mrSql = "INSERT INTO mr (mr, ocurrences, length, proteinId, qtyOcurrences) VALUES (@mr, @ocurrences, @length, @proteinId, @qtyOcurrences)";
    sqlite3_prepare_v2(db,  mrSql.c_str(), 512, &mrStatement, NULL);

    for (auto& file: files) {
        string proteinFilename = file.path().generic_string();
        FastaParser f = FastaParser(proteinFilename);

        for(auto& protein: f.getProteins()) {
            //Parse proteins and insert them into the DB
            insertProtein(proteinStatement, protein.first, proteinFilename, protein.second, familyName);
            records++;
            pushed++;

            //Run mrs for protein
            Mrs m = Mrs::runMrs(protein.first, '+', 0);
            for(auto& ocurr: *(m.getOcurrences())) {
                vector<string> v;
                
                for(auto& position: ocurr.second) {
                    v.emplace_back(std::to_string(position));
                }

                string ocurrenceList = boost::algorithm::join(v,", ");
                string qtyOcurrences = std::to_string(v.size());
                insertMrData(mrStatement, std::to_string(ocurr.first.length()), getProteinId(db, protein.first), ocurrenceList, ocurr.first, qtyOcurrences);
                records++;
            }

        }
    }

    createIndexes(db);
    sqlite3_exec(db, "END TRANSACTION", NULL, NULL, &error);
    sqlite3_close(db);

    cout << "There are " << pushed << " proteins loaded." << endl;
    cout << "Imported " << records << " records in "<< (clock() - cStartClock) / (double)CLOCKS_PER_SEC << " seconds" << endl;

    sqlite3_shutdown();
    return 0;
}