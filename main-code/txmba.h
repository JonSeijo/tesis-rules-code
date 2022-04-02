/**
 * Generates transactions suitable for analyzing with the apriori algorithm (via an R package) for 
 * Market Basket Analysis knowledge discovery.
 */
#include <vector>
#include <map>
#include <unordered_set>
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <sstream>
#include <stdio.h>
#include <regex>
#include <utility>
#include <exception>
#include <chrono>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string/join.hpp>
#include "parse.h"

#ifndef TXMBA_H
#define TXMBA_H

using namespace std;

namespace fs = boost::filesystem;

/**
 * Object that creates transactions for MBA from MRs of proteins
 */
class Txmba
{
    friend class TxmbaTest;

    protected:
        unsigned int processed;
        fs::path path;
        string familyName;
        unsigned int minLength;
        unsigned int limit;
        unsigned int minOcurrences;
        ofstream outputFile;
        ofstream notopened;
        string outputFilename;

	public:
		Txmba(fs::path path, string familyName, unsigned int minLength, unsigned int minOcurrences, unsigned int limit, string outputFilename);
        Txmba(const Txmba& other);
        ~Txmba();
        static Txmba createFromParams(int argc, char* argv[]);
        virtual void generateTransactions();
        string displaySummary();
        bool isLimitReached();
        virtual void processProtein(pair<string,string>& protein, string proteinFilename);
        void pushProtein(vector<string> proteinTxData);
};


class TxmbaBag: public Txmba
{
    protected:
        string mrData;
        Mrs mr;
        std::vector< std::list<string> > proteinWithMrs;
        std::vector<string> proteinDirectory;
        std::vector<int> proteinIndexForMrJoinedPositions;
        unsigned int computedLimit;

        string joinProteinsToFile(const char* path);

    public:
        TxmbaBag(fs::path path, string familyName, unsigned int minLength, unsigned int minOcurrences, unsigned int limit, string outputFilename);
        TxmbaBag(const TxmbaBag& other);
        TxmbaBag(TxmbaBag&& other) = default;
        ~TxmbaBag();
        static TxmbaBag createFromParams(int argc, char* argv[]);
        void processProtein(pair<string,string>& protein, string proteinFilename);
        void generateTransactions();
};

#endif // TXMBACLEA_H