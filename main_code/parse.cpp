#include "parse.h"

////////// FastaParser //////////

FastaParser::FastaParser(string fname)
{
    filename = fname;
    string protein = string();
    string comment = string();
    std::ifstream infile(filename.c_str(), std::ifstream::in);
    std::string line;
    int lineNumber = 0;

    //Get length of file
    infile.seekg (0, infile.end);
    int length = infile.tellg();
    infile.seekg (0, infile.beg);

    if(length > 0) {
        while (std::getline(infile, line)) {
            std::istringstream iss(line);
            string currentLine = iss.str();

            if(currentLine.length()>0) {
                char first = currentLine[0];
                if(first != '>') { //ignore first
                    protein = protein + currentLine;
                } else {
                    if(lineNumber>0) { //Reading a new comment, then push both protein and comment
                        protein.erase(std::remove(protein.begin(), protein.end(), '\n'), protein.end());
                        proteins.push_back(make_pair(protein, comment));
                    }
                    comment = currentLine;
                    protein = string();
                }
                lineNumber++;
            }
        }
    }

    //Push last item read to internal data structures
    protein.erase(std::remove(protein.begin(), protein.end(), '\n'), protein.end());
    proteins.push_back(make_pair(protein, comment));
    infile.close();
}

string FastaParser::getFilename()
{
  return filename;
}

string FastaParser::getProtein()
{
  return proteins[0].first;
}

string FastaParser::getComment()
{
  return proteins[0].second;
}

vector<ProteinAndComment> FastaParser::getProteins()
{
  return proteins;
}

////////// MRS //////////

Mrs::Mrs(const Mrs& m)
{
    this->stringToAnalyze = m.stringToAnalyze;
    this->output = m.output;
    this->ocurrences = m.ocurrences;
    this->lengths = m.lengths;
}

void Mrs::writeOutputToFile(string path, string data)
{
    ofstream out;
    out.open(path);
    out << data;
    out.close();
}

string Mrs::readFileIntoString(string filename)
{
    string content = string();
    std::ifstream infile(filename.c_str(), std::ifstream::in);
    std::string line;

    //Get length of file
    infile.seekg (0, infile.end);
    int length = infile.tellg();
    infile.seekg (0, infile.beg);
    content.reserve(length);

    if(length > 0) {
        while (std::getline(infile, line)) {
            std::istringstream iss(line);
            string currentLine = iss.str() + "\n";

            if(currentLine.length()>0) {
                content.append(currentLine);
            }
        }
    }

    //Push last item read to internal data structures
    //content.erase(std::remove(content.begin(), content.end(), '\n'), content.end());
    infile.close();
    return content;
}

/**
 * Initialize the object with the output of the runmrs.py (or runmrsFromFile.py) program
 */
Mrs::Mrs(string mrsOutput, string path)
{
    this->output = mrsOutput;

    std::regex rmrs("([A-Za-z]+)\\s+(\\(\\d+\\))");
    std::regex rpositions("[0-9]+");
    std::istringstream f(this->output);
    std::string line;


    string m;
    while (std::getline(f, line)) {
        std::smatch sm;
        bool match = std::regex_match(line, sm, rmrs);

        if(match) {
            string result = sm[2];
            result.erase(std::remove(result.begin(), result.end(), '('), result.end());
            result.erase(std::remove(result.begin(), result.end(), ')'), result.end());
            m = sm[1];
            this->lengths[m] = std::stoi(result);

        } else {
            std::regex_token_iterator<std::string::iterator> rend;
            std::regex_token_iterator<std::string::iterator> iter ( line.begin(), line.end(), rpositions );
            while (iter != rend) {
                this->ocurrences[m].push_back(std::stoi(*iter)); //Store the positions where MRs ocurr
                iter++;
            }
        }
    } //end while

   // cout << "Having... " << this->ocurrences.size() << " MRs computed" << endl;
}

string Mrs::cmd; //Define this variable otherwise get linker error!

string Mrs::prepareCommand(string stringToAnalyze, char separator, int minLength)
{
    //Initialize cmd variable
    Mrs::cmd = "python ../turjanski/findpat/pyapi/runmrs.py";
    return Mrs::cmd + " \""+ stringToAnalyze +"\" " + separator + " " + std::to_string(minLength);
}

string Mrs::runCommand(string command)
{
    //cout << "Running command...  '" << command << "'" << endl;
    char buffer[512];
    string result = "";
    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) throw std::runtime_error("popen() failed!");
    try {
        while (!feof(pipe)) {
            if (fgets(buffer, 512, pipe) != NULL)
                result += buffer;
      }
    } catch (...) {
      pclose(pipe);
      throw;
    }
    pclose(pipe);
    return result;
}

string Mrs::prepareFileCommand(string filename, char separator, int minLength)
{
    //Initialize cmd variable
    Mrs::cmd = "python ../turjanski/findpat/pyapi/runmrsFromFile.py";
    return Mrs::cmd + " \""+ filename +"\" " + separator + " " + std::to_string(minLength);
}

Mrs Mrs::createMrsFromCommand(string command, string outputFile)
{
    string result;
    fs::path cachedFile(outputFile);
    if(outputFile != "" && fs::exists(cachedFile) && fs::file_size(cachedFile)>1) {
        result = Mrs::readFileIntoString(outputFile);
        return Mrs(result);    
    } else {
        result = Mrs::runCommand(command);    
        if(outputFile != "") {
            writeOutputToFile(outputFile, result);
        } else {
            writeOutputToFile("runmrs.out", result);
        }
        
        return Mrs(result);
    }
}


Mrs Mrs::runMrsFromFile(string stringFilename, char separator, int minLength, string mrsCommandExitFilename)
{
    string command = Mrs::prepareFileCommand(stringFilename, separator, minLength);
    return Mrs::createMrsFromCommand(command, mrsCommandExitFilename);
}


Mrs Mrs::runMrs(string stringToAnalyze, char separator, int minLength)
{
    //cout << "Preparing MRs for string of length: " << stringToAnalyze.length() << endl;
    string command = Mrs::prepareCommand(stringToAnalyze, separator, minLength);
    return Mrs::createMrsFromCommand(command);
}

string Mrs::getOutput()
{
    return this->output;
}

map<string, vector<int> >* Mrs::getOcurrences()
{
    return &(this->ocurrences);
}

map<string, int>* Mrs::getLengths()
{
    return &(this->lengths);
}

vector<string> Mrs::m(unsigned int length)
{
    vector<string> mr;
    for (map<string, int>::iterator it = this->lengths.begin() ; it != this->lengths.end(); ++it) {
        if(it->first.length() >= length) {
            mr.push_back((it->first));
        }
    }

    return mr;
}

/**
 * Cleans a pathname of "/"
 * @param  fs::path path the path whose pathname is to be cleaned
 * @return string the cleaned pathname
 */
string Mrs::cleanPath(fs::path path) 
{
    string pathQueried = path.generic_string();
    pathQueried.erase(std::remove_if(pathQueried.begin(), pathQueried.end(), [](char x){return x == '/' || x == '.';}),
               pathQueried.end());

    return pathQueried;
}

/**
 * Joins proteins form a path to a file. It appends the suffix "-joined" to the output file.
 * @param  const char* filePath
 * @return string the pathname of the joined file.
 */
string Mrs::joinProteinsToFile(const char* filePath)
{
    fs::path path(filePath);

    if(!exists(path) || !is_directory(path)) {
        throw new std::exception();
    }

    string pathQueried = Mrs::cleanPath(path);
    string joinedFilename = pathQueried+"-joined.txt";

    fs::path joinedPath(joinedFilename);
    if(!fs::exists(joinedPath) || fs::file_size(joinedPath)<1) {
        //If no joined file exsists, get all the proteins from folder, parse and joined them into a file.
        fs::recursive_directory_iterator begin(path), end;
        std::vector<fs::directory_entry> files(begin, end);

        //std::vector<string> v(files.size(), ""); //Maybe optimal
        std::vector<string> v;

        int pushed = 0;
        for(auto& file: files) {
            FastaParser f = FastaParser(file.path().generic_string());
            for(auto& proteinAndComment: f.getProteins()) {
                v.push_back(proteinAndComment.first);
                pushed++;
            }
        }

        //cout << "There are " << pushed << " proteins loaded." << endl;
        string joined = boost::algorithm::join(v,"+");
        
        ofstream joinedFile;
        joinedFile.open(joinedFilename);
        joinedFile << joined;
        joinedFile.close();
    }

    return joinedFilename;
}

//////////// Famico ////////////

/**
 * Computes the coverage of a string s in relation with a sequence taking into account
 * elements of length >= minimumLengthToConsider
 * @param  string& s                        the string to check for coverage in sequences
 * @param  std::vector<string>& sequences   the sequences to find the coverage
 * @param  int minimumLengthToConsider      min length to consider
 * @return double the computed coverage
 */
double Famico::coverage(const string& s, const std::vector<string>& sequences, int minimumLengthToConsider)
{
    vector<int> v(s.length(),-1);
    for (vector<string>::const_iterator it = sequences.begin(); it != sequences.end(); ++it) {
        string target = (*it);
        
        int targetLength = target.length();
        vector<int> positions;

        //Get the ocurrences...
        size_t pos = s.find(target, 0);
        while(pos != string::npos) {
            positions.push_back(pos);
            pos = s.find(target,pos+1);
        }

        for (vector<int>::iterator itPositions = positions.begin(); itPositions != positions.end(); ++itPositions) {
            int pos = (*itPositions);
            for(int i = 0; i < targetLength; i++) {
                if(v[pos+i] == -1 || targetLength < v[pos+i]) {
                    v[pos+i] = targetLength;
                }
            }
        }
    }

    int numerator = s.length();

    for (vector<int>::iterator it = v.begin() ; it != v.end(); ++it) {
        //cout << endl << " IT : " << (*it) << endl;
        if((*it) < minimumLengthToConsider) {
            numerator--;  
        }
    }    
    v.clear();

    //cout << endl << " n/d : " << (double)numerator << "/" << (double)s.length() << endl;
    return (double)numerator/(double)s.length();
}

double Famico::familiarity(string s, string t)
{
    Mrs mrsForT = Mrs::runMrs(t, '+', 0);
    double familiarity = (Famico::coverage(s, mrsForT.m(0)) + Famico::coverage(s, mrsForT.m(s.length())))/2;
    for(unsigned int i = 1; i < s.length(); i++) {
        familiarity += Famico::coverage(s, mrsForT.m(i));
    }
    return familiarity;
}