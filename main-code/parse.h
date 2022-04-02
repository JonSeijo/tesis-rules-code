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

#ifndef PARSE_H
#define PARSE_H

using namespace std;

namespace fs = boost::filesystem;

typedef pair<string,string> ProteinAndComment;

/**
 * Parser for .FASTA files (or multi-FASTA)
 */
class FastaParser
{
    protected:
        string filename;
		vector<ProteinAndComment> proteins;

	public:
		FastaParser(string filename);
		string getFilename();
        string getProtein();
		string getComment();
		vector<ProteinAndComment> getProteins();
};

/**
 * MRs processing functions for strings.
 */
class Mrs
{
    friend class MrsTest;

    protected:
        string stringToAnalyze;
        string output;
        map<string, vector<int> > ocurrences;
        /**
         * ocurrences = {
         *     MR_i : [ pos_i0, ... , pos_ik]
         *     MR_j : [ pos_j0, ... , pos_jl]
         * }
         */
        map<string, int> lengths;

	public:
        static string cmd;
		
        Mrs() {};
        Mrs(string mrsOutput, string path = "runmrs.out");
        Mrs(const Mrs& m);

        static void writeOutputToFile(string path, string data);
        static string readFileIntoString(string filename);
        static string prepareCommand(string stringToAnalyze, char separator, int minLength);
        static string runCommand(string command);
        static string prepareFileCommand(string filename, char separator, int minLength);
        static Mrs createMrsFromCommand(string command, string output = "");
        static Mrs runMrs(string stringToAnalyze, char separator, int minLength);
        static Mrs runMrsFromFile(string stringFilename, char separator, int minLength, string mrsCommandExitFilename = "");
        static string joinProteinsToFile(const char* path);
        static string cleanPath(fs::path path);
        
        map<string, vector<int> >* getOcurrences(); //returns the dictionary of ocurrences.
        map<string, int>* getLengths();
        vector<string> m(unsigned int length); //returns the MRs of length >= length (parameter)
        string getOutput();
};

/**
 * Familiarity and coverage functions
 */
class Famico
{
    public:
        static double coverage(const string& s, const vector<string>& sequences, int minimumLengthToConsider = 0);
        static double familiarity(string s, string t);
};

#endif // PARSE_H