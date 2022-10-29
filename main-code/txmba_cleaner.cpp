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
 * @param string outputFilename where to store the cleaned output
 */
TxmbaCleaner::TxmbaCleaner(const string &inputFile, const string &outputFilename) {
	this->inputFilename = inputFile;
    this->outputFile.open(outputFilename);
}

/**
 * Process each line of the file and clean it
 */
void TxmbaCleaner::cleanLines(CleanMode cleanMode) {
    int txsCleaned = 0;

    std::ifstream infile(this->inputFilename.c_str(), std::ifstream::in);
    std::string line;

    //Get length of file
    infile.seekg (0, infile.end);
    int length = infile.tellg();
    infile.seekg (0, infile.beg);

    if (length > 0) {
        while (std::getline(infile, line)) {
            txsCleaned++;
            if (txsCleaned % 1000 == 0) {
                std::cout << "Transactions cleaned: " << txsCleaned << std::endl;
            }
            std::istringstream iss(line);
            string currentLine = iss.str();
            if (currentLine.length()>0) {
                string cleaned = cleanLine(cleanMode, currentLine);
                if (cleaned.length()>0) {
                    this->writeLineToFile(cleaned);
                }
            }
        }
    }

    infile.close();
    outputFile.close();
}

string TxmbaCleaner::cleanLine(CleanMode cleanMode, string &line) {
    switch (cleanMode) {
        case CleanMode::substring:
            return this->cleanExclusion(line);
        case CleanMode::superstring:
            return this->cleanInclusion(line);
        case CleanMode::minimum:
            return this->cleanMinimum(line);
        default:
            throw std::invalid_argument("Invalid cleanMode");
    }
}

bool contains(const string &haystack, const string &needle) {
    return haystack.find(needle) != std::string::npos;
}

string TxmbaCleaner::cleanInclusion(const string &itemsLine) {
    vector<string> items = buildItems(itemsLine);
    list<string> res = filterItemsWithMode(items, false);
    return boost::algorithm::join(res, ",");
}

string TxmbaCleaner::cleanExclusion(const string &itemsLine) {
    vector<string> items = buildItems(itemsLine);
    list<string> res = filterItemsWithMode(items, true);
    return boost::algorithm::join(res, ",");
}

// TODO: Sigue siendo horrible
list<string> TxmbaCleaner::filterItemsWithMode(const vector<string> &items, bool removeContained) {
    vector<pair<string, bool>> results = buildItemsWithPresentStatus(items);
    for (auto &result : results) {
        if (result.second) {
            for (auto &comp : results) {
                if (&result.first != &comp.first && comp.second) {
                    if (contains(result.first, comp.first)) {
                        if (removeContained) {
                            result.second = false;
                        } else {
                            comp.second = false;
                        }
                    }
                }
            }
        }
    }
    return getItemsPresent(results);
}

vector<string> TxmbaCleaner::buildItems(const string &itemsLine) {
    vector<string> items;
    boost::split(items, itemsLine, boost::is_any_of(","));
    return items;
}

vector<pair<string, bool>> TxmbaCleaner::buildItemsWithPresentStatus(const vector<string> &items) {
    vector< pair<string, bool> > results(items.size());
    for(auto& elem: items) {
        results.emplace_back(pair<string, bool>(elem, true));
    }
    return results;
}

list<string> TxmbaCleaner::getItemsPresent(vector<pair<string, bool>>& results) {
    list<string> res;
    for (auto & result : results) {
        if (result.second) {
            res.emplace_back(result.first);
        }
    }
    return res;
}

string TxmbaCleaner::cleanMinimum(const string &line) {
    assert(0 && "Not implemented!");
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