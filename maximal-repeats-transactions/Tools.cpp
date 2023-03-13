#include "Tools.h"



string Tools::getFilename(const string s){
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




bool Tools::loadMultifastaFile(const string filename, const string family, vector<FastaElement>& fs){
  bool ret=true;
  // File open
  ifstream is(filename.c_str());
  if(!is.good()){
      cout << "Error! function " << __FUNCTION__ << " cannot open " << filename << endl;
      ret=false;
  }
  else{
    
      // load protein 
      char c;
      if(!is.eof()) {
	    is >> c;
	    if(c!='>') {
		    cout << "Error! function " << __FUNCTION__ << " ! Multifasta file has an incorrect format." << endl;
		    return 1;
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
	    f.family=family;
	    fs.push_back(f);
      }
      is.close();
  }
  return ret;

}


bool Tools::loadFastaFilesFromFolder(const string folder, const string family, vector<FastaElement>& fs, const bool deleteNonCanonicalAminoacidProteins){

  if(system(("find "+folder+" -name '*.fasta' -print0 | xargs -r -0 ls -1 > _ls.tmp").c_str())!=0) {
    cout << "Error! function " << __FUNCTION__ << " cannot execute ls command!" << endl;
    return false;
  }
  string temporalFileName="_ls.tmp";
  // File open
  ifstream is(temporalFileName.c_str());
  if(!is.good()){
      cout << "Error! Function " << __FUNCTION__ << "It's not possible to open " << temporalFileName << endl;
      return false;
  }
  
  set<char> nonCanonicalAminoacids;
  set<string> proteinsWithNonCanonicalAminoacids;
  // Load files from each multifasta at ls
  while(!is.eof()) {
      string proteinFileName;
      getline(is,proteinFileName);
      if(proteinFileName!="") {
	  vector<FastaElement> aux_ps;
	  bool ok;
	  ok=Tools::loadMultifastaFile(proteinFileName,family, aux_ps);
	  if(!ok) return false;
	  if(aux_ps.size()!=1){
              cout << "Error! Function " << __FUNCTION__ << " . " << proteinFileName << " is not fasta file. It's a MULTIFASTA! This file has " << aux_ps.size() << " proteins. The problem resides at the moment to assign the name (it always assigns the filename)." << endl;
              return false;
          }
          else{
            // Only one protein
            bool atLeastOne = Tools::toCanonicalAminoacids(aux_ps[0], '+', nonCanonicalAminoacids);
            if(atLeastOne) {
                proteinsWithNonCanonicalAminoacids.insert(aux_ps[0].name);
                if(!deleteNonCanonicalAminoacidProteins) fs.push_back(aux_ps[0]); 
            }
            else{
                fs.push_back(aux_ps[0]);
            }
          }
          
    }
  }
  is.close();
  
  cout << "Summary" << endl;
  cout << "-------"  << endl;
  cout << endl;
  cout << "Family: " << family << endl;
  cout << "non-canonical aminoacids: ";
  for (std::set<char>::iterator it = nonCanonicalAminoacids.begin(); it != nonCanonicalAminoacids.end(); ++it){
    cout << *it << " "; 
  }
  cout << endl;
  cout << "proteins with non-canonical aminoacids           : " << proteinsWithNonCanonicalAminoacids.size() << endl;
  cout << "proteins with non-canonical aminoacids (ratio)   : ";
  if(deleteNonCanonicalAminoacidProteins) cout << ( (1.0 * proteinsWithNonCanonicalAminoacids.size()) / (proteinsWithNonCanonicalAminoacids.size()+ fs.size())) << endl;
  else cout << ( (1.0 * proteinsWithNonCanonicalAminoacids.size()) / fs.size()) << endl;
  cout << "Eliminate proteins with non-canonical aminoacids : " << (deleteNonCanonicalAminoacidProteins?"True":"False") << endl;
  cout << endl;
  

  
  if(system(("rm "+temporalFileName).c_str())!=0) {
    cout << "Error function " << __FUNCTION__ << " cannot execute rm command! " << endl;
    return false;
  }
  
  return true;

}



bool Tools::toCanonicalAminoacids(FastaElement& f, const char separatorChar, set<char>& nonCanonicalAminoacids){
    string canonicalAminoacids="ACDEFGHIKLMNPQRSTVWY";
    bool atLeastOne=false;
    for(unsigned int i=0;i<f.seq.size();i++){
        if (canonicalAminoacids.find(f.seq[i]) == std::string::npos){
            // not found as canonical aminoacids
            nonCanonicalAminoacids.insert(f.seq[i]); // to report
            f.seq[i]=separatorChar; // replace nonCanonicalAminoacid by separatorChar
            atLeastOne=true;
        }
    }
    
//     if(atLeastOne){
//         cout << "non canonical letters: ";
//         for (std::set<char>::iterator it = nonCanonicalLetters.begin(); it != nonCanonicalLetters.end(); ++it){
//             cout << *it << " "; 
//         }
//     }
    
    return (atLeastOne);
    
}


bool Tools::loadProteins(const string inputFileName, vector<FastaElement>& fs, vector<string>& families){  
  ifstream is(inputFileName.c_str());
  if(!is.good()) {
    cout << "Error function " << __FUNCTION__ << " . "<< inputFileName << " can't be opened." << endl;
    return false;
  }
  
  // load header 
  if(!is.eof()){
    string headerTemplate="family|folder";
    string header;
    getline(is,header);
    if(header!=headerTemplate){
      cout << "Error function " << __FUNCTION__ << " . File header " << inputFileName << " (" << header << ") differs from the expected (" << headerTemplate << ")." << endl;
      return false;
    }
  }
  else{
    cout << "Error function " << __FUNCTION__ << ". File " << inputFileName << " is empty." << endl;
    return false;
  }
  
  // for each row load proteins
  int fsSize=0;
  while(!is.eof()){
      // proteins family
      string family;
      getline(is,family,'|');
      if(family!=""){
	// folder
	string folder;
	getline(is,folder);
	// load information
	if(folder!=""){
	  bool ok;
	  ok=Tools::loadFastaFilesFromFolder(folder, family, fs, false);
	  if(!ok) return false;
	  cout << "family: " << family << " \t - folder: " << folder << " \t - # proteins: " << (fs.size()-fsSize) << endl;
	  fsSize=fs.size();
	}
      }
  }
  
  
  // families resume
  map<string,int> familiesResume;
  for(int i=0;i<(int)fs.size();i++){
    if(familiesResume.find(fs[i].family)==familiesResume.end()){
      familiesResume[fs[i].family]=1;
    }
    else{
      familiesResume[fs[i].family]++;
    }
  } 
  
  cout << endl;
  cout << "families resume: " << endl;
  for (std::map<string,int>::iterator it=familiesResume.begin(); it!=familiesResume.end(); ++it){
    std::cout << "family: " << it->first << " \t => #proteins:  " << it->second << endl;
    families.push_back(it->first);
  }
  
  
  
  
  
  return true;
}



bool Tools::loadRunmrsOutput(const string filename, vector< pair< string, vector<unsigned long int> >  >& rs){
  bool ret=true;
  ifstream is(filename.c_str());
  if(!is.good()){
      cout << "Error! Function " << __FUNCTION__ << " . " << filename << " can't be opened." << endl;
      ret=false;
  }
  else{
      // load file 
      while(!is.eof()){
	    string seq,s;
	    vector<unsigned long int> starts;
	    is >> seq;
	    if(seq!=""){
		  getline(is,s); // reject "length string". This data is implicit in the string seq 
		  // load "starts string"
		  getline(is,s); 
		  istringstream ss(s);
		  while(!ss.eof()){
		    unsigned long int start;
		    ss >> start;
		    starts.push_back(start);
		  }
		  //sort starts list from lowest to highest
		  // O(n log n)
		  std::sort (starts.begin(), starts.end()); 
		  // save result
		  rs.push_back(pair< string, vector<unsigned long int> >(seq, starts));
	    }
      }
      is.close();
  }
  return ret;
}


bool Tools::executeRunmrs(const string s, vector< pair< string, vector<unsigned long int> >  >  & rs, const int minimunRepeatLength){
  bool ok=true;
   
  
  ofstream os("__seqRunmrsFromFile.dat.tmp");
  if(!os.good()){
    cout << "Error! Function " << __FUNCTION__ << " . Temporal file __seqRunmrsFromFile.dat.tmp can't be opened." << endl;
    return false;
  }
  os << s;
  os.close();
  
  // Important: runmrsFromFile.py always uses '+' as separator! 
  if(system(("python runmrsFromFile.py __seqRunmrsFromFile.dat.tmp + "+Tools::toString(minimunRepeatLength)+"  > _runmrs.tmp").c_str())!=0) {
    cout << "Error! Function " << __FUNCTION__ << " cannot execute runmrs!" << endl;
    return false;
  }

  // Read the output
  ok = loadRunmrsOutput("_runmrs.tmp", rs);
  if(!ok) {
    cout << "Error! Function " << __FUNCTION__ << " cannot read the runmrs output file (_runmrs.tmp)!" << endl;
    return false; 
  }
  
 
  return ok;

}



vector<string> Tools::gnuplotColorsPaletteSpecific1(){    
  vector<string> ret;
  ret.push_back("#FF0000");     // red
  ret.push_back("#0000FF");     // blue
  ret.push_back("#008000");     // green 
  ret.push_back("#7F7F7F");     // gray
  ret.push_back("#00FFFF");     // cyan
  ret.push_back("#FF00FF");     // magenta
  ret.push_back("#A52A2A");     // brown
  ret.push_back("#FFA500");     // organge
  
  
  ret.push_back("#87CEFA");     // lightskyblue
  ret.push_back("#C71585");     // mediumvioletred
  ret.push_back("#ADFF2F");     // greenyellow
  ret.push_back("#778899");     // lightslategray
  ret.push_back("#008B8B");     // darkcyan
  ret.push_back("#8B008B");     // darkmagenta
  ret.push_back("#9370DB");     // mediumpurple
  ret.push_back("#BC8F8F");     // rosybrown 
  ret.push_back("#FF4500");     // orangered
  
  ret.push_back("#CD5C5C");     // indianred
  ret.push_back("#00FFFF");     // aqua
  ret.push_back("#006400");     // darkgreen
  ret.push_back("#A9A9A9");     // darkgray
  ret.push_back("#E0FFFF");     // lightcyan
  ret.push_back("#FF00FF");     // fuschsia
  ret.push_back("#4B0082");     // indigo
  ret.push_back("#D2691E");     // chocolate
  ret.push_back("#FFA07A");     // lightsalmon
  
  ret.push_back("#DC143C");     // crimson
  ret.push_back("#483D8B");     // darkslateblue
  ret.push_back("#228B22");     // forestgreen
  ret.push_back("#C0C0C0");     // silver
  ret.push_back("#00CED1");     // darkturquoise
  ret.push_back("#EE82EE");     // violet
  ret.push_back("#FF69B4");     // hotpink
  ret.push_back("#B8860B");     // darkgoldenrod 
  ret.push_back("#FF7F50");     // coral

  
  ret.push_back("#FFB6C1");     // lightpink
  ret.push_back("#0000CD");     // mediumblue
  ret.push_back("#00FF00");     // lime
  ret.push_back("#708090");     // slategray

  
  return ret;
}
