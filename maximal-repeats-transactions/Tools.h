#ifndef TOOLS_H
#define TOOLS_H

#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <fstream>
#include <stdlib.h>
#include <algorithm>

#include "FastaElement.h"

using namespace std;


class Tools{
  public:
    // file loader
    static bool loadMultifastaFile(const string filename, const string family, vector<FastaElement>& fs);
    static bool loadFastaFilesFromFolder(const string folder, const string family, vector<FastaElement>& fs, const bool deleteNonCanonicalAminoacidProteins);
    static bool loadProteins(const string inputFileName, vector<FastaElement>& fs, vector<string>& families);
    
    static bool loadRunmrsOutput(const string filename, vector< pair< string, vector<unsigned long int> >  >& rs);
    static bool executeRunmrs(const string s, vector< pair< string, vector<unsigned long int> >  >  & candidatosAFactores, const int minimaLongitudPatron);

    // data type conversion
    template<typename T>
    static string toString(const T x){ostringstream ss; ss << x; return ss.str();};
    static int toInt(const char* s){int ret;istringstream is(s);is >> ret;return ret;};

    // data manipulation
    static string getFilename(const string s);
    
    // gnuplot colour palette
    static vector<string> gnuplotColorsPaletteSpecific1();
    
private:
    static bool toCanonicalAminoacids(FastaElement& f, const char separatorChar, set<char>& nonCanonicalAminoacids);

  

};
#endif // TOOLS_H