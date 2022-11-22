#include <iostream>
#include <fstream>
#include <vector>
#include "parse.h"
#include <boost/filesystem.hpp>
#include <boost/algorithm/string/join.hpp>
 
namespace fs = boost::filesystem;

string cleanPath(fs::path path) 
{
    string pathQueried = path.generic_string();
    pathQueried.erase(std::remove(pathQueried.begin(), pathQueried.end(), '/'),
               pathQueried.end());

    return pathQueried;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " path\n";
        return 1;
    }
 
    fs::path path(argv[1]);
    if(!exists(path) || !is_directory(path)) {
        std::cout << path << " is not a path\n";
        return 1;
    }
 
    string pathQueried = cleanPath(path);
    string joinedFamilyStringFilename = Mrs::joinProteinsToFile(argv[1]);
    
    //MRs for the family...
    cout << "Running runmrsFromFile from PyApi..." << endl;
    Mrs joinedMrs = Mrs::runMrsFromFile(joinedFamilyStringFilename, '+', 0);

    FastaParser inka = FastaParser("ikba/P25963.fasta");
    string proteinToAnalyze = inka.getProtein();

    //Save results to file
    ofstream resultados;
    resultados.open(pathQueried+"-coverage-resultados.txt");

    for(int i = 0; i<11; i++) {
        //cout << "Computing coverage for protein for size M(i) with i = " << i << endl;
        resultados << i << ',' << Famico::coverage(proteinToAnalyze, joinedMrs.m(i), i) << endl;
    }

    //cout << joined << endl;
    resultados.close();
}