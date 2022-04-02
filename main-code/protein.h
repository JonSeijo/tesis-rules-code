#include <map>
#include <string>
#include <iostream>

#ifndef PROTEIN_H
#define PROTEIN_H

using namespace std;

class Protein
{
	protected:
		string encoding;
		string filename;

	public:
	    Protein(string enc, string fname = "");
		const string getEncoding() const;
		map<char,int> getAminoSummary();
		int getLength();
		const string getFilename() const;

		/*
		bool operator==(const Protein& l) const;
		bool operator!=(const Protein& l) const;
		*/

		static void combineSummary(const map<char,int>& freqInfo, map<char,int>& acumulator);
};

#endif // PROTEIN_H
