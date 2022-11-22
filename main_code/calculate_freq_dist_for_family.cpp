/**
 * Calcula la distribucion de caracteres para una carpeta de proteinas.
 */

#include <iostream>
#include <sstream>
#include <string>
#include <boost/filesystem.hpp>
#include "protein.h"
#include "parse.h"
#include <boost/algorithm/string/join.hpp>
 // or <experimental/filesystem> in new compilers
 
namespace fs = boost::filesystem;

using namespace std;

/**
 * Receive a pathname, a family name and a streaming output and
 * calculate the frequency of aminoacids distribution
 * @param const string& proteinFolderName folder name to where extract the proteins stored in the folder
 * @param const string& familyName        name to identify the family
 * @param ofstream& out the output streaming to write the results into a file
 */
void calculateFrequencyForProteinsInPath(const string& proteinFolderName, const string& familyName, ofstream& out)
{
    fs::path proteinFolder(proteinFolderName);
    if(!exists(proteinFolder) || !is_directory(proteinFolder)) {
        cerr << proteinFolder << " is not a path\n";
    }

    //Search for proteins, and insert them
    fs::recursive_directory_iterator begin(proteinFolder), end;
    std::vector<fs::directory_entry> files(begin, end);
    //std::vector<string> v(files.size(), ""); //Maybe optimal
    
    unsigned int pushed = 0;
    unsigned int totalLength = 0;

    map<char,int> result;
    for (auto& file: files) {
        string proteinFilename = file.path().generic_string();
        FastaParser f = FastaParser(proteinFilename); //Parse the protein

        for(auto& proteinRead: f.getProteins()) {
            Protein prot = Protein(proteinRead.first);
            Protein::combineSummary(prot.getAminoSummary(), result);
            totalLength += prot.getLength();
            pushed++;
        }
    }

    if(totalLength > 0) {
        for (auto& entry: result) {
            out << familyName << "\t" << entry.first << "\t" << double(entry.second) / double(totalLength) << endl;
        }
    }

    cout << " - Processed " << pushed << " proteins for " << familyName << "." << endl;
}

void processCustomList(ofstream& out)
{
    string dir = "../../data/proteins/familyDataset/";

    std::map<string,string> list;

    /*
    list["ABCtran"] = dir+string("ABCtran");
    list["Arm"] = dir+string("Arm");
    list["CorA"] = dir+string("CorA");
    list["Fer4"] = dir+string("Fer4");
    list["Globin"] = dir+string("Globin");
    list["HEAT"] = dir+string("HEAT");
    list["Hexapep"] = dir+string("Hexapep");
    list["Ldlreceptb"] = dir+string("Ldlreceptb");
    list["MIP"] = dir+string("MIP");
    list["mixScrambled"] = dir+string("mixScrambled");
    list["Nebulin"  ] = dir+string("Nebulin"  );
    list["PBP" ] = dir+string("PBP" );
    list["PeptidaseC25"] = dir+string("PeptidaseC25");
    list["Pkinase"] = dir+string("Pkinase");
    list["PUD"] = dir+string("PUD");
    list["Sel1"] = dir+string("Sel1");
    list["TPR1"] = dir+string("TPR1");
    list["wd"] = dir+string("wd");
    list["ank"] = dir+string("ank");
    list["CWbinding1"] = dir+string("CWbinding1");
    list["Filamin"] = dir+string("Filamin");
    list["Glycohydro19"] = dir+string("Glycohydro19");
    list["HelicaseC"] = dir+string("HelicaseC");
    list["Kelch1"] = dir+string("Kelch1");
    list["LRR1"] = dir+string("LRR1");
    list["Mitocarr"] = dir+string("Mitocarr");
    list["mixUniformDistributed"] = dir+string("mixUniformDistributed");
    list["NEWAnk"] = dir+string("NEWAnk");
    list["PD40"] = dir+string("PD40");
    list["PFLlike"] = dir+string("PFLlike");
    list["PPbinding"] = dir+string("PPbinding");
    list["PUF"] = dir+string("PUF");
    list["TerB"] = dir+string("TerB");
    list["TSP1"] = dir+string("TSP1");
    list["YadAhead"] = dir+string("YadAhead");
    list["Annexin"] = dir+string("Annexin");
    list["Collagen"] = dir+string("Collagen");
    list["dehalogenase"] = dir+string("dehalogenase");
    list["GDCP"] = dir+string("GDCP");
    list["GreAGreB"] = dir+string("GreAGreB");
    list["HemolysinCabind"] = dir+string("HemolysinCabind");
    list["Ldlrecepta"] = dir+string("Ldlrecepta");
    list["MgtE"] = dir+string("MgtE");
    list["mix"] = dir+string("mix");
    list["MORN"] = dir+string("MORN");
    list["NEWWD40"] = dir+string("NEWWD40");
    list["Pentapeptide"] = dir+string("Pentapeptide");
    list["PIN"] = dir+string("PIN");
    list["PPR"] = dir+string("PPR");
    list["Rhomboid"] = dir+string("Rhomboid");
    list["Thaumatin"] = dir+string("Thaumatin");
    list["ValtRNAsyntC"] = dir+string("ValtRNAsyntC");
    */
    
    list["ank-uniform"] = dir+string("ank-uniform");
    list["ank-scrambled"] = dir+string("ank-scrambled");

    for(auto& l: list) {
        calculateFrequencyForProteinsInPath(l.second, l.first, out);
    }
}

int main(int argc, char* argv[])
{
    //Initialize file to store results
    string outputFile = "freq-dist.txt";
    ofstream resultados;
    resultados.open(outputFile, std::ios_base::out);
    resultados << "fam" << "\t" << "let" << "\t" << "fr" << endl; //Write header to file

    if(argc == 2 && string(argv[1]).compare("--batch") == 0) {
        processCustomList(resultados);
    } else if (argc < 3) {
        cout << "Usage: " << argv[0] << " path familyName " << endl;
        return 1;
    } else {
        string familyName = string(argv[2]);
        //Calculate freq dist for parameters received
        calculateFrequencyForProteinsInPath(string(argv[1]), familyName, resultados);
    }

    resultados.close();
    return 0;
}