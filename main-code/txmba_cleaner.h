/**
 * Several functions for reading fasta files, computing MRs from functions (through external app and 
 * familiariy and coverage functions)
 */
#include <vector>
#include <map>
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <sstream>
#include <stdio.h>
#include <regex>
#include <utility>
#include <exception>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string/join.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <boost/range/algorithm.hpp>
#include <boost/range/algorithm_ext.hpp>
#include "parse.h"

#ifndef TXMBACLEANER_H
#define TXMBACLEANER_H

using namespace std;

namespace fs = boost::filesystem;

enum CleanMode {
    substring = 0, // exclusion
    superstring = 1, // inclusion
    minimum = 2 // exact
};

/**
 * Cleaner for MBA transactions.
 * Depending on the mode it will clean either for:
 *   inclusion (or superstring mode),
 *   exclusion (or substring mode),
 *   minimum (or exact mode),
 */
class TxmbaCleaner {
    friend class TxmbaCleanerTest;

    protected:
        string cleanLine(CleanMode cleanMode, string &line);

        string cleanInclusion(const string &line);
        string cleanExclusion(const string &line);
        string cleanMinimum(const string &line);

        static void writeLinesToFile(vector<string> &lines, const string &outputFilename);
        static list<string> getItemsPresent(vector<pair<string, bool>> &results) ;
        static vector<string> buildItems(const string &itemsLine);
        static vector<pair<string, bool>> buildItemsWithPresentStatus(const vector<string> &items);
        static list<string> cleanTransactionsWithInclusionExclusion(const vector<string> &items, bool removeContained);
        static list<string> cleanTransactionsWithMinimum(const vector<string> &transaction);

	public:
		TxmbaCleaner();
        void cleanLines(CleanMode cleanMode, const string &inputFile, const string &outputFilename);


};

#endif // TXMBACLEANER_H