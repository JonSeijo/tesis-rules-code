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

/**
 * Cleaner for MBA transactions.
 * Depending on the mode it will clean either for inclusion (or superstirng mode) or exclusion (or substring mode)
 */
class TxmbaCleaner
{
    friend class TxmbaCleanerTest;

    protected:
        string inputFilename;
        ofstream outputFile;
        string cleanInclusion(string in);
        string cleanExclusion(string in);
        bool inclusion = true;

        void writeLineToFile(string line);

	public:
		TxmbaCleaner(string inputFilename, bool inclusionMode, string outputFilename);
        TxmbaCleaner(const TxmbaCleaner& other);
        void cleanLines();
        
};

#endif // TXMBACLEANER_H