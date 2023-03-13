#ifndef MER_H
#define MER_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <set>
#include <map>
#include <vector>

#include "sais.h"
#include "Tools.h"
#include "FastaElement.h"



using namespace std;


class txmers {

    private:
        unsigned char *T;
        int *SA;
        int *LCP;  
        unsigned int *proteinID;
        long n;

        void computeSA();
        void computeLCP();
        void computeTxs(const unsigned int amountOfProteins, const unsigned int minLengthOfPattern, const unsigned int maxLengthOfPattern, const unsigned int minNumberOfAffectedProteins);
        void txsInicialization(const unsigned int amountOfProteins);
        void emptyTxsDeletion(const unsigned int amountOfProteins);
        void l_intervals(vector<unsigned int> &l, vector<unsigned int> &i, vector<unsigned int>& j);
        void computeTailleferPatternsAndTx(const unsigned int minLengthOfPattern, const unsigned int maxLengthOfPattern, const unsigned int minNumberOfAffectedProteins);
       
        void addOccurrence(map<char, unsigned int> &map1, char e);
        void addPatternToTransactions(map<unsigned int, set<string> >&  txs, const unsigned int i, const unsigned int j, const string & pattern, const unsigned int minNumberOfAffectedProteins);
        unsigned int numberOfaffectedProteins(map<unsigned int, set<string> >&  txs, const unsigned int i, const unsigned int j, const string & pattern);

    public:
        // From Taillefer
        map<unsigned int, set<string> > SMR_txs;
        map<unsigned int, set<string> >  NN_txs;
        map<unsigned int, set<string> >  NE_txs;


        string setName;
        void printSAandLCP();
        
        // Constructor
        txmers(const string& inputFastaFolderName, const string& sn, const unsigned int minLengthOfPattern, const unsigned int maxLengthOfPattern, const unsigned int minNumberOfAffectedProteins);
        ~txmers();
        
};

#endif // MER_H


