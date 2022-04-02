/**
 * Crea archivos con transacciones a partir de leer proteínas de una carpeta.
 * Cada transacción tiene (MRi, MRi+1, ..., MRi+k, IDFamilia)
 * donde IDFamilia es un parámetro del programa como así también cuantas veces tiene
 * que repetir un MRi para que sea incluído y a partir de qué longitud de MRs se considera.
 *
 * Los MRs se consideran a partir de cada proteína.
 */

#include <iostream>
#include <sstream>
#include <string>
#include <boost/filesystem.hpp>
#include "parse.h"
#include <boost/algorithm/string/join.hpp>
 // or <experimental/filesystem> in new compilers
 
namespace fs = boost::filesystem;

using namespace std;

int main(int argc, char* argv[])
{
    unsigned int minLength = 2;
    unsigned int minOcurrences = 1;
    unsigned int limit = 0;

    if (argc < 3) {
        cout << "Usage: " << argv[0] << " path familyName minLength (defaults to 2) minOcurrences (default to 1)" << endl;
        return 1;
    }
 
    
    string pathQueried = string(argv[1]);
    fs::path p(argv[1]);
    if(!exists(p) || !is_directory(p)) {
        cerr << p << " is not a path\n";
        return 1;
    }


    string familyName = string(argv[2]);
    
    if(argc > 3) {
        istringstream ss(argv[3]);
        if (!(ss >> minLength))
            cerr << "Invalid number " << argv[3] << '\n';
    } 

    if(argc > 4) {
        istringstream ss(argv[4]);
        if (!(ss >> minOcurrences))
            cerr << "Invalid number " << argv[4] << '\n';
    } 

    if(argc > 5) {
        istringstream ss(argv[5]);
        if (!(ss >> limit))
            cerr << "Invalid number " << argv[5] << '\n';
    }

    string outputFile = pathQueried+"-tx-mba.txt";
    if(argc > 6) {
        outputFile = string(argv[6]);
    }

    //Initialize file to store results
    ofstream resultados;
    resultados.open(outputFile, std::ios_base::app | std::ios_base::out);
    
    //Not opened proteins
    ofstream notopened;
    notopened.open("not.txt", std::ios_base::app | std::ios_base::out);

    //Search for proteins, and insert them
    fs::recursive_directory_iterator begin(p), end;
    std::vector<fs::directory_entry> files(begin, end);
    //std::vector<string> v(files.size(), ""); //Maybe optimal
    
    unsigned int pushed = 0;

    for (auto& file: files) {
        string proteinFilename = file.path().generic_string();
        FastaParser f = FastaParser(proteinFilename); //Parse the protein

        for(auto& protein: f.getProteins()) {

            //For each protein, run mrs, store tx data in a file    
            Mrs m = Mrs::runMrs(protein.first, '+', minLength);
            vector<string> proteinTxData;
            bool shouldPush = false;
            for(auto& ocurr: *(m.getOcurrences())) {
                if(ocurr.second.size() >= minOcurrences) {
                    proteinTxData.emplace_back(ocurr.first);
                    shouldPush = true;
                }
            }

            //Store family name in tx
            proteinTxData.emplace_back(familyName);

            if(shouldPush) {
                if(familyName.compare("-") != 0) {
                    proteinTxData.emplace_back(familyName);
                }

                //Store tx data in a file
                string tx = boost::algorithm::join(proteinTxData, ",");
                resultados << tx << endl;
                pushed++;
            } else {
                notopened << proteinFilename << endl;
            }
        }

        if(limit > 0 && limit == pushed) {
            break;
        }
    }


    cout << " - There are " << pushed << " tx created for " << familyName << "." << endl;

    resultados.close();
    return 0;
}