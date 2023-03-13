#include "txmers.h"


txmers::txmers(const string& inputFastaFolderName, const string& sn, const unsigned int minLengthOfPattern, const unsigned int maxLengthOfPattern, const unsigned int minNumberOfAffectedProteins){
    setName=sn;
    bool ok;
    vector<FastaElement> fs;
    ok=Tools::loadFastaFilesFromFolder(inputFastaFolderName, setName, fs,true);
    if(!ok) fprintf(stderr, "Class txmers->loadFastaFilesFromFolder: Error!\n");
    
    
    std::cout << "Loaded " << fs.size() << " FastaElements" << std::endl;
    
    //1. total=#aminoacids
    unsigned int total=0;
    for(unsigned int iProtein=0;iProtein<fs.size();iProtein++){
        total+=fs[iProtein].seq.size();
    }
    
    std::cout << "Assigning memory ..." << std::endl;
    //2. memory assignment = total+#separatorSymbols+2  (2=endTerminatorSymbol$ and endTerminatorSymbol|)
    n=total+fs.size()+2;
    T         = (unsigned char *)malloc((size_t)n * sizeof(unsigned char));
    proteinID = (unsigned int  *)malloc((size_t)n * sizeof(unsigned int ));
    //3. Copy aminoacids+separatorSymbols to T
    unsigned int iPos=0;
    for(unsigned int iProtein=0;iProtein<fs.size();iProtein++){
        for(unsigned int iSeq=0;iSeq<fs[iProtein].seq.size();iSeq++){
            T[iPos]        =fs[iProtein].seq[iSeq];
            proteinID[iPos]=iProtein;
            iPos++;
        }
        T[iPos]        ='+';
        proteinID[iPos]=-1;
        iPos++;
   }
   T[iPos]        ='$';
   proteinID[iPos]=-1;
   iPos++;
   T[iPos]        ='|'; // > Alphabet (used by l_intervals algorithm)
   proteinID[iPos]=-1;

   std::cout << "Computing SA ..." << std::endl;
   computeSA();
   std::cout << "Computing LCP ..." << std::endl;
   computeLCP();
   std::cout << "Computing TXs ..." << std::endl;
   computeTxs(fs.size(), minLengthOfPattern, maxLengthOfPattern, minNumberOfAffectedProteins);
    
//    printSAandLCP();    

    
}
    
    
    
void txmers::computeTxs(const unsigned int amountOfProteins, const unsigned int minLengthOfPattern, const unsigned int maxLengthOfPattern, const unsigned int minNumberOfAffectedProteins){
    txsInicialization(amountOfProteins);
    computeTailleferPatternsAndTx(minLengthOfPattern, maxLengthOfPattern, minNumberOfAffectedProteins);
    emptyTxsDeletion(amountOfProteins);
}
    
    
void txmers::txsInicialization(const unsigned int amountOfProteins){
            for(unsigned int iProtein=0;iProtein<amountOfProteins;iProtein++){
                SMR_txs[iProtein]=set<string>();
                 NN_txs[iProtein]=set<string>();
                 NE_txs[iProtein]=set<string>();
            }
}    
    
void txmers::emptyTxsDeletion(const unsigned int amountOfProteins){
            for(unsigned int iProtein=0;iProtein<amountOfProteins;iProtein++){
                if(SMR_txs[iProtein].empty()) SMR_txs.erase(iProtein);
                if( NN_txs[iProtein].empty())  NN_txs.erase(iProtein);
                if( NE_txs[iProtein].empty())  NE_txs.erase(iProtein);
            }
}    

/* Construct the suffix array. */
void txmers::computeSA(){
    SA  = (int *)malloc((size_t)n * sizeof(int));
    if(SA == NULL) {
        fprintf(stderr, "Class txmers->computeSA: Cannot allocate memory.\n");
        exit(EXIT_FAILURE);
    }
    if(sais(T, SA, (int)n) != 0) {
        fprintf(stderr, "Class txmers->computeSA->sais: Cannot allocate memory.\n");
        exit(EXIT_FAILURE);
    }
}

void txmers::computeLCP(){
    // require SA computed
    // ... naive LCP:
    LCP = (int *)malloc((size_t)n * sizeof(int));

    if(LCP == NULL) {
        fprintf(stderr, "Class txmers->computeLCP: Cannot allocate memory.\n");
        exit(EXIT_FAILURE);
    }

    for (int iSA = 1; iSA < n; ++iSA) {
        int l = 0;
        while ((T[SA[iSA]+l]==T[SA[iSA-1]+l]) &&  T[SA[iSA]+l]!='+') ++l;
        LCP[iSA] = l;
    }

    // In order to avoid border cases in repeat classification, assigns
    //    ... LCP[0]=0
    LCP[0]=0;
}   








/////////////////////////  Print
void txmers::printSAandLCP(){
  fprintf(stderr,"\n");
  // print SA  
  fprintf(stderr,"==============================\n");
  fprintf(stderr,"   SA    ; LCP; Suff \n");
  fprintf(stderr,"==============================\n");

  for(int iSA=0;iSA<n;iSA++){
    fprintf(stderr," SA[%d]=%d ; ",iSA, SA[iSA]);
     if(iSA!=0) fprintf(stderr," %d ; ",LCP[iSA]);
     else fprintf(stderr," - ; ");
    for(int ipos=SA[iSA];ipos<n;ipos++) fprintf(stderr,"%c",T[ipos]);

    fprintf(stderr,"\n");
  }
  fprintf(stderr,"==============================\n\n");
}


txmers::~txmers(){
  free(T);
  free(LCP);
  free(SA);
}


void txmers::addOccurrence(map<char, unsigned int> &map1, char e)
{
    if(map1.find(e) != map1.end()){
        // AL SEPARADOR + le damos un tratamiento distinto! S\'olo puede tener una instancia. Son todos distintos entre s\'i
        if(e!='+') map1[e]++;  
    }    
    else{
        map1.insert(map<char,unsigned int>::value_type(e,1));
    }
}


void txmers::l_intervals(vector<unsigned int> &vector_l, vector<unsigned int> &vector_i, vector<unsigned int>& vector_j){
    
    vector<unsigned int> interval_l;
    vector<unsigned int> interval_i;
    vector<unsigned int> interval_j;
    
    interval_l.push_back(0);
    interval_i.push_back(0);
    interval_j.push_back(0); // NULL
    for(unsigned int i=1;i<=n;i++){
        unsigned int lb = i - 1;
        while (LCP[i] < (int)interval_l[interval_l.size()-1]){
            interval_j[interval_j.size()-1]=i-1;
            
            vector_l.push_back(interval_l[interval_l.size()-1]);
            vector_i.push_back(interval_i[interval_i.size()-1]);
            vector_j.push_back(interval_j[interval_j.size()-1]);
            
            
            lb = interval_i[interval_i.size()-1];
            interval_l.pop_back();
            interval_i.pop_back();
            interval_j.pop_back();
            
        }
        if(LCP[i] > (int) interval_l[interval_l.size()-1]){
            interval_l.push_back(LCP[i]);
            interval_i.push_back(lb);
            interval_j.push_back(0); // NULL
        }
    }
}



void txmers::computeTailleferPatternsAndTx(const unsigned int minLengthOfPattern, const unsigned int maxLengthOfPattern, const unsigned int minNumberOfAffectedProteins){
    // require SA, LCP
    
    // 1. Compute Intervals
    vector<unsigned int> ls;
    vector<unsigned int> is;
    vector<unsigned int> js;
    l_intervals(ls, is, js);
        
    // 2. Parameter set
    LCP[0]=0; // Ojo, es de prueba!    

    // 3. each pattern classification 
    for(unsigned int it=0;it<is.size();it++){ 
        unsigned int l=ls[it];
        unsigned int i=is[it];
        unsigned int j=js[it];
        
        if( (l>=minLengthOfPattern) && (l<=maxLengthOfPattern)){
            // pattern
            string pattern="";
            for(unsigned int isuff=0;isuff<l;isuff++) pattern+=(T[SA[i]+isuff]); 
            char sigma = T[SA[i]-1];  // Any pattern left context to next
                                    // check if they are all the same
            bool is_MR = (sigma=='+'); // is_MR flag inicialization.
                                    // If sigma is a separator then it's a MR

            // Survey of left & right context
            map<char, unsigned int> LCTT, RCTT; // empty dictionaries
            for(unsigned int k=i;k<=j;k++){
                char sigma_l=T[SA[k]-1]; // left  context
                char sigma_r=T[SA[k]+l]; // right context
                addOccurrence(LCTT, sigma_l);
                addOccurrence(RCTT, sigma_r);
                // l-interval always contains at least one element 
                // that is not right extensible (by definition)
                // We only need to check if it's not left-extensible
                if(sigma!=sigma_l) 
                    is_MR = true; // It's not left-extensible then it is a MR
            }

            if(is_MR){  // Is it SMR, NN or NE?
                // MR is a SMR?
                // There is not pair of occurrences that has the same left or right-context
                // Then, they cant't be extended
                bool cantBeExtended = true;
                for ( std::map<char,unsigned int>::iterator it = LCTT.begin(); it != LCTT.end() && cantBeExtended; ++it){
                    cantBeExtended = (cantBeExtended && (it->second<=1));
                }
                for ( std::map<char,unsigned int>::iterator it = RCTT.begin(); it != RCTT.end() && cantBeExtended; ++it){
                    cantBeExtended = (cantBeExtended && (it->second<=1));
                }

                if(cantBeExtended) {
                    addPatternToTransactions(SMR_txs, i, j, pattern, minNumberOfAffectedProteins); // It is SMR;
                }
                else{   // Is it NN or NE?
                    // Find an occurrence that is not right and left extensible
                    // If it exist then it is a NN
                    bool isNested = true;
                    for(unsigned int k=i;(k<=j) && isNested;k++){ // For each occurence ...
                        char sigma_l=T[SA[k]-1];
                        char sigma_r=T[SA[k]+l];
                        if( (LCTT[sigma_l]<=1) && (RCTT[sigma_r]<=1) ){
                            // This occurence is not right and left extensible
                            isNested = false;
                        }
                    }
                    if(isNested) { addPatternToTransactions(NE_txs, i, j, pattern, minNumberOfAffectedProteins); // It is a NE
                                                    // (all pattern occurrence are nested)
                    }
                    else         { addPatternToTransactions(NN_txs, i, j, pattern, minNumberOfAffectedProteins); // It is a NN
                                                    // (At least one pattern occurrence is non-nested)
                    }
                }
            } 
        }
    }
}




void txmers::addPatternToTransactions(map<unsigned int, set<string> >&  txs, const unsigned int i, const unsigned int j, const string & pattern, const unsigned int minNumberOfAffectedProteins){

    if(numberOfaffectedProteins(txs, i, j, pattern)>=minNumberOfAffectedProteins)
    // for each pattern occurrence
    for(unsigned int iSA=i;iSA<=j;iSA++){
        // It finds the pattern proteinID
        unsigned int pID=(proteinID[SA[iSA]]);
        // Add the pattern to de tx 
        txs[pID].insert(pattern);
    }
    
    
}


unsigned int txmers::numberOfaffectedProteins(map<unsigned int, set<string> >&  txs, const unsigned int i, const unsigned int j, const string & pattern){
    
    set<unsigned int> affectedProteins; 
    // for each pattern occurrence
    for(unsigned int iSA=i;iSA<=j;iSA++){
        // It finds the pattern proteinID
        unsigned int pID=(proteinID[SA[iSA]]);
        // Add proteinID
        affectedProteins.insert(pID);
    }
    
    return affectedProteins.size();
    
}
