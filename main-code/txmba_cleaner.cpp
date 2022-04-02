#include "txmba_cleaner.h"

/**
 * Copy constructor
 * @param TxmbaCleaner& other
 */
TxmbaCleaner::TxmbaCleaner(const TxmbaCleaner& other)
{
	//Initialize file to store results
    //this->outputFile.open(outputFilename, std::ios_base::app | std::ios_base::out);
    //this->outputFile.open(other.outputFile);
}

/**
 * Creates a new instance of the class
 * @param string inputFile the file where to read the transactions to be cleaned
 * @param bool inclusionMode whether to clean for inclusion or exclusion
 * @param string outputFilename where to store the cleaned output
 */
TxmbaCleaner::TxmbaCleaner(string inputFile, bool inclusionMode, string outputFilename)
{
	this->inputFilename = inputFile;
    this->outputFile.open(outputFilename);
    this->inclusion = inclusionMode;
}


/**
 * Process each line of the file and clean it
 */
void TxmbaCleaner::cleanLines()
{
    std::ifstream infile(this->inputFilename.c_str(), std::ifstream::in);
    std::string line;

    //Get length of file
    infile.seekg (0, infile.end);
    int length = infile.tellg();
    infile.seekg (0, infile.beg);

    if(length > 0) {
        while (std::getline(infile, line)) {
            std::istringstream iss(line);
            string currentLine = iss.str();
            string cleaned;
            if(currentLine.length()>0) {
                if(inclusion) {
                    cleaned = this->cleanInclusion(currentLine);
                } else {
                    cleaned = this->cleanExclusion(currentLine);
                }

                if(cleaned.length()>0) {
                    this->writeLineToFile(cleaned);
                }
            }
        }
    }

    infile.close();
    outputFile.close();
}


/**
 * Clean the current line with a specific criteria
 * @param string line
 */
string TxmbaCleaner::cleanInclusion(string line)
{
    vector<string> aux;
    boost::split(aux, line, boost::is_any_of(","));
    vector< pair<string, bool> > results(aux.size());
    for(auto& a: aux) {
        results.emplace_back(pair<string, bool>(a, true));
    }

    for (vector<pair<string, bool> >::iterator it = results.begin() ; it != results.end(); ++it) {
        for (vector<pair<string, bool>>::iterator comp = results.begin() ; comp != results.end();) {
            if(&(*it).first != &(*comp).first && (*comp).second != false) {
                if((*it).first.find((*comp).first) != string::npos) {
                    (*comp).second = false;
                }
            }
            ++comp;
        }
    }

    list<string> res;
    for (vector<pair<string, bool> >::iterator it = results.begin() ; it != results.end(); ++it) {
        if((*it).second) {
            res.emplace_back((*it).first);
        }
    }
    
    return boost::algorithm::join(res, ",");
}

/**
 * Clean the current line with a specific criteria
 * @param string line
 */
string TxmbaCleaner::cleanExclusion(string line)
{
    vector<string> aux;
    boost::split(aux, line, boost::is_any_of(","));
    vector< pair<string, bool> > results(aux.size());
    for(auto& a: aux) {
        results.emplace_back(pair<string, bool>(a, true));
    }

    for (vector<pair<string, bool> >::iterator it = results.begin() ; it != results.end(); ++it) {
        if((*it).second != false) {
            for (vector<pair<string, bool>>::iterator comp = results.begin() ; comp != results.end();) {
                if(&(*it).first != &(*comp).first && (*comp).second != false) {
                    if((*it).first.find((*comp).first) != string::npos) {
                        (*it).second = false;
                    }
                }
                ++comp;
            }
        }
    }

    list<string> res;
    for (vector<pair<string, bool> >::iterator it = results.begin() ; it != results.end(); ++it) {
        if((*it).second) {
            res.emplace_back((*it).first);
        }
    }
    
    return boost::algorithm::join(res, ",");
}

/**
 * Write processed line to file
 * @param string line
 */
void TxmbaCleaner::writeLineToFile(string line)
{
    line.erase(std::remove(line.begin(), line.end(), '\n'), line.end());
    this->outputFile << line << endl;
}