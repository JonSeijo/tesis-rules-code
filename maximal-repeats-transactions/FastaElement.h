#ifndef FASTAELEMENT_H
#define FASTAELEMENT_H

#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <stdio.h>
#include <sstream>
#include <fstream>




using namespace std;

class FastaElement {
    private:
        vector<unsigned int> startPositions(const string& s) const;
        string getFilename(const string s) const;


    
    
    public:

	string name;
	string description;
	string seq; 
	string family;
	bool operator==(const FastaElement &f2) const;  

	// Constructor
	FastaElement();
        
        bool loadFromFastaFile(const string filename, const string familyName);

        // functions
        set< pair< string, vector<unsigned int> >  >  positionsOverMe(const set<string>& sequence) const;
        double coverage      (const set< pair< string, vector<unsigned int> >  >&  positionsOverTestSeq, const unsigned int minimunRepeatLength) const;
        double familiarity_10(const set< pair< string, vector<unsigned int> >  >&  positionsOverTestSeq) const;
};

// Output
ostream& operator <<(ostream& os, const FastaElement& );
#endif // FASTAELEMENT_H
