#include "FastaElement.h"

FastaElement::FastaElement(){
	name="";
	description="";
	seq="";
	family="";
}


bool FastaElement::operator==(const FastaElement&f2) const{
	return (seq==f2.seq);
};


ostream& operator <<(ostream& os, const FastaElement& f){
	os << "> " << f.description << " - family: " << f.family << endl;
        os << f.seq << endl;
        return os;
};



set< pair< string, vector<unsigned int> >  >  FastaElement::positionsOverMe(const set<string>& sequence) const{
    set< pair< string, vector<unsigned int> >  >  res=set< pair< string, vector<unsigned int> >  >();  //<pattern,< startPositions over fasta sequence> >
    set<string>::iterator si;
    
    for(si = sequence.begin(); si!=sequence.end(); si++){
	
        string s=*si;
	vector<unsigned int> positions = startPositions(s);
	if((int)positions.size()>0){
	  res.insert(pair< string, vector<unsigned int> >(s,positions));
	}
    }
    return res;
}

vector<unsigned int> FastaElement::startPositions(const string& s) const{
  vector<unsigned int> res;
  if(seq.size()>=s.size()){
     size_t pos = seq.find(s, 0);
     while(pos != string::npos)
     {
        res.push_back((unsigned int)pos);
        pos = seq.find(s,pos+1);
     }
  }
  return res;
}
  
  


double FastaElement::coverage(const set< pair< string, vector<unsigned int> >  >&  positionsOverTestSeq, const unsigned int minimunRepeatLength) const{
    // initialization
    vector<bool> affectedPositions;
    for(unsigned int i=0;i<seq.size();i++) affectedPositions.push_back(false);
    
    // mark with true affected positions
    set< pair< string, vector<unsigned int> >  >::iterator si_poss;
    for(si_poss=positionsOverTestSeq.begin();si_poss!=positionsOverTestSeq.end();si_poss++){
        string s=(*si_poss).first;
        vector<unsigned int> positions=(*si_poss).second;
        if(s.size()>=minimunRepeatLength){
  	  // add +1 all places repetition appear 
	  for(unsigned int istart=0;istart<positions.size();istart++){
	    unsigned int start=positions[istart];
	    unsigned int end  =start+s.size()-1;
	    for(unsigned int k=start;k<=end;k++) affectedPositions[k]=true;
	  }
        }
    }
    
    //count affected positions
    double ret=0;
    for(unsigned int i=0;i<affectedPositions.size();i++){
        //fprintf(stderr," %d \n",affectedPositions[i]?1:0);
        if(affectedPositions[i]) ret=ret+1.0;
    }
    return (ret/seq.size());
}
  
  
  
double FastaElement::familiarity_10(const set< pair< string, vector<unsigned int> >  >&  positionsOverTestSeq) const{
    double sum=0;
    for(unsigned int i=1;i<10;i++) sum+=coverage(positionsOverTestSeq, i);
    return ( (1+coverage(positionsOverTestSeq, 10))/2.0 + sum );
}





bool FastaElement::loadFromFastaFile(const string filename, const string familyName){
    
  

  vector<FastaElement> fs;
  // File Open 
  ifstream is(filename.c_str());

  if(!is.good()){
      cout << "Error! function " << __FUNCTION__ << " cannot open " << filename << endl;
      return false;
  }
  else{
    
      // Load protein (if there are more than one, all of them are loaded into fs)
      char c;
      if(!is.eof()) {
	    is >> c;
	    if(c!='>') {
		    cout << "Error! function " << __FUNCTION__ << " ! Multifasta file has an incorrect format." << endl;
		    return false;
	    }
      }
      while(!is.eof()){
	    FastaElement f;
	    f.name=getFilename(filename); // delete path and extension from filename
	    getline(is,f.description);
	    is >> c;
	    while((!is.eof()) && (c!='>')){
		    f.seq+=c;
		    is >> c;
	    }
	    f.family=familyName;
	    fs.push_back(f);
      }
      is.close();
  }
  
  
  // Only one protein?
  if(fs.size()!=1){
      cout << "Error! Function " << __FUNCTION__ << " . " << filename << " is not fasta file. It's a MULTIFASTA! This file has " << fs.size() << " proteins. The problem resides at the moment to assign the name (it always assigns the filename)." << endl;
      return false;
  }
    
  // f is the unique protein in the file
  FastaElement f=fs[0];
    
  // assign f to this
  name=f.name;
  description=f.description;
  seq=f.seq;
  family=familyName;  
  
  return true;

}



string FastaElement::getFilename(const string s) const{
  ///////////////////////////////////////////////////  
  //     delete path and extension from filename   // 
  ///////////////////////////////////////////////////
  string fileName;
  // fileName bars counter
  int barsCounter=0;
  for(int icb=0;icb<(int)s.size();icb++) if(s[icb]=='/') barsCounter++;
  istringstream ss(s);
  // Remove all before bars
  for(int icb=0;icb<barsCounter;icb++) getline(ss,fileName,'/');
  // Remove extension
  getline(ss,fileName,'.');
  return fileName;
}
