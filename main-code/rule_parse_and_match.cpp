#include "rule_parse_and_match.h"


/**
 * Copy constructor
 * @param RuleParser& other
 */
RuleParser::RuleParser(const RuleParser& other)
{
	//Initialize file to store results
    //this->outputFile.open(outputFilename, std::ios_base::app | std::ios_base::out);
    //this->outputFile.open(other.outputFile);
}

/**
 * Creates a new instance of the class
 * @param string inputFile the input rule file
 * @param string proteinDirectory the files where to read the proteins
 * @param string outDirectory the place where to store the matched protein files
 */
RuleParser::RuleParser(string inputFile, string proteinDirectory, string outDirectory)
{
	this->inputFilename = inputFile;
    this->proteinRootFolder = proteinDirectory;
    this->proteins = loadProteins();
    this->proteinMatchOutDir = outDirectory;
}

/**
 * Load proteins from protein directory.
 * @return a vector with the Protein objects loaded
 */
vector<Protein> RuleParser::loadProteins()
{
    vector<Protein> v;

    //Open folder of proteins and for each one generate a transaction
    fs::recursive_directory_iterator begin(this->proteinRootFolder), end;
    std::vector<fs::directory_entry> files(begin, end);
    
    //For each file, get the proteins and process them
    for (auto& file: files) {
        string proteinFilename = file.path().generic_string();
        FastaParser f = FastaParser(proteinFilename); //Parse the protein
        for(pair<string,string>& protein: f.getProteins()) {
            v.emplace_back(Protein(protein.first, proteinFilename));
        }
    }

    return v;
}

/**
 * Read the file of the rules. For each line parse it as a Rule
 * and run the function createProteinFileMatchForRule().
 * Once every line is read and analyzed process the alignment files
 */
void RuleParser::processRuleFile()
{
    std::ifstream infile(this->inputFilename.c_str(), std::ifstream::in);
    std::string line;

    //Get length of file
    infile.seekg (0, infile.end);
    int length = infile.tellg();
    infile.seekg (0, infile.beg);

    if(length > 0) {
        while (std::getline(infile, line)) {
            std::istringstream iss(line);
            string rule = iss.str();
            if(rule.length()>0) {
                createProteinFileMatchForRule(rule);
            }
        }
    }
    infile.close();

    processAlignementFiles();
}

/**
 * From a given string line containing a rule, generate
 * a vector of the items that belong to that rule for later processing.
 * @param string line
 * @return vector<string> of the items that make up that rule
 */
itemlist RuleParser::parseRule(string line)
{
    itemlist v;
    size_t pos = line.find("=>");
    line.replace(pos, 2, ",");
    line.erase(std::remove_if(line.begin(), 
                              line.end(),
                              [](char x){return std::isspace(x) || x == '{' || x == '}';}),
               line.end());
    
    
    boost::split(v, line, boost::is_any_of(","));
    return v;
}

/**
 * From a rule as string parse it into a vector of items and then match
 * each of those items against the bulk of proteins. 
 * If there is a match, save the protein and the filename into the file
 * that contains the rule and the proteins that match
 * @param string rule
 */
void RuleParser::createProteinFileMatchForRule(string rule)
{
    bool headerWritten = false;
    ofstream ruleMatchFile;
    itemlist parsedItemsFromLine = parseRule(rule);
    string ruleConsequent = extractConsequentFromParsedRule(parsedItemsFromLine);
    string formattedRule = boost::algorithm::join(parsedItemsFromLine,"-");
    string ruleMatchFilename = proteinMatchOutDir + formattedRule + string(".txt");
    
    ruleMatchFile.open(ruleMatchFilename);

    for(auto& proteinObj: proteins) {
        if(matchItemsAgainstProtein(proteinObj.getEncoding(), parsedItemsFromLine)) {
            if(!headerWritten) {
                headerWritten = true;
                ruleMatchFile << rule << endl << endl;
            }
            ruleMatchFile << proteinObj.getFilename() << "," << proteinObj.getEncoding() << endl;

            //Match the consequent against the proteins (if the whole itemlist matched, the consequent matches trivially)
            unsigned int matchedSubsequence = 0; //This is to differentiate multiple matches inside the same protein because this is not really an aligment problem
            for(auto& aligned: getAlignedSequences(proteinObj.getEncoding(), ruleConsequent)) {
                std::string sequenceName = formattedRule + string("-") + std::to_string(matchedSubsequence) + string("-") + string(basename(proteinObj.getFilename().c_str()));
                matchedSubsequence++;
                //Store alignements in a list for further processing
                consequentAlignements[ruleConsequent].emplace_back(sequenceName + string("\t") + aligned);
            }
        }
    }


    ruleMatchFile.close();
}

/**
 * Creates alignement files (in stockholm 1.0 format XXX.sto)
 */
void RuleParser::processAlignementFiles()
{
    for(auto& consequentAndLines: consequentAlignements) {
        ofstream alignFile;
        alignFile.open(proteinMatchOutDir + consequentAndLines.first + string(".sto"));
        alignFile << "# STOCKHOLM 1.0" << endl << endl; //Write header for .sto @see https://en.wikipedia.org/wiki/Stockholm_format

        for(auto& lines: consequentAndLines.second) {
            alignFile << lines << endl;
        }

        alignFile << "//";
        alignFile.close();
    }
}

/**
 * Check that a list is fully contained inside a protein encoding
 * @param string proteinEncoding
 * @param itemlist items
 * @return bool whether it matches or not
 */
bool RuleParser::matchItemsAgainstProtein(const string& proteinEncoding, const itemlist& items)
{
    bool matched = true;
    for(auto& item: items) {
        if(proteinEncoding.find(item) == string::npos) {
            matched = false;
            break;
        }
    }

    return matched;
}

/**
 * Extract consequent from a given rule
 * @param  const itemlist& ruleItems the parsed rule and itemset
 * @return string
 */
string RuleParser::extractConsequentFromParsedRule(const itemlist& ruleItems)
{
    return ruleItems[ruleItems.size()-1];
}

/**
 * Takes a fragment of a protein and the full enconding and padds it with
 * the rest of the context of the protein if available and returns it in a vector
 * @param const string& proteinEncoding the full enconding of the protein
 * @param const string& fragment the fragment to search for its context
 * @return vector<string>
 */
vector<string> RuleParser::getAlignedSequences(const string& proteinEncoding, const string& fragment)
{
    vector<string> v;
    int offset = fragment.size();

    size_t pos = proteinEncoding.find(fragment);
    while(pos != string::npos) {
        string match = "";
        match.reserve(fragment.size()+2+PADDING);

        for(int pleft = 0; pleft < PADDING; pleft++) {
            int index = pos - PADDING + pleft;
            if(index >= 0) {
                match.append(1, proteinEncoding[index]);        
            } else {
                match.append("X");
            }
        }

        match.append(fragment);

        for(int pright = 0; pright < PADDING; pright++) {
            unsigned int index = pos + offset + pright;
            if(index < proteinEncoding.length()) {
                match.append(1, proteinEncoding[index]);        
            } else {
                match.append("X");
            }
        }

        v.emplace_back(match);
        pos = proteinEncoding.find(fragment, pos+1);
    }

    return v;
}