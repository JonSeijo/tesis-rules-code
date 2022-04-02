/**
 * Functions for generating scrambled or uniform protein data
 * for testing purposes.
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
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <random>

#ifndef SCRAMBLER_H
#define SCRAMBLER_H

#define AMINO_ACID_COUNT 20
#define MODE_SCRAMBLE 1
#define MODE_UNIFORM 2

using namespace std;

namespace fs = boost::filesystem;

/**
 * Scrambler class that scrambles proteins and also
 * generates a uniform mix of the data set send as input.
 */
class Scrambler
{
    friend class ScramblerTest;

    protected:
        fs::path inputDirectory;
        string outputDirectory;
        int getRandomAminoAcidCode();
        fs::path createPathObject(string dir);
        bool replace(string& s, const string& from, const string& to);

	public:
        static const char aminoAcids[20];

		Scrambler(string input, string output);
        //Scrambler(const Scrambler& other);
        string scramble(string input);
        string uniform(int length);
        void generateVariations(int mode);
};

#endif // SCRAMBLER_H