/**
 * Functions for parsing protein rule files and matching them against actual proteins
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
#include "protein.h"

#ifndef RULEPARSER_H
#define RULEPARSER_H

#define PADDING 2

using namespace std;

namespace fs = boost::filesystem;

typedef vector<string> itemlist;

/**
 * Parses MBA rule files
 */
class RuleParser
{
    friend class RuleParseTest;

    protected:
        string inputFilename;
        string proteinRootFolder;
        string proteinMatchOutDir;
        vector<Protein> proteins;
        map<string, list<string> > consequentAlignements;

        vector<Protein> loadProteins();
        itemlist parseRule(string line);
        bool matchItemsAgainstProtein(const string& proteinEncoding, const itemlist& items);
        void createProteinFileMatchForRule(string currentLine);
        string extractConsequentFromParsedRule(const itemlist& ruleList);
        vector<string> getAlignedSequences(const string& proteinEncoding, const string& fragment);
        void processAlignementFiles();

    public:
        RuleParser(string inputFilename, string proteinDirectory, string outDirectory);
        RuleParser(const RuleParser& other);
        void processRuleFile();
        
};

#endif // RULEPARSER_H