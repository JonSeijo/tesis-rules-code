#include "txmba.h"

/**
 * Copy constructor
 * @param Txmba& other
 */
Txmba::Txmba(const Txmba& other)
{
	//Parameters
	this->path = other.path;
	this->familyName = other.familyName;
	this->minLength = other.minLength;
	this->minOcurrences = other.minOcurrences;
	this->limit = other.limit;
	this->outputFilename = other.outputFilename;

	//Initialize file to store results
    this->outputFile.open(other.outputFilename, std::ios_base::app | std::ios_base::out);
    
    //Not opened proteins
    this->notopened.open("not.txt", std::ios_base::app | std::ios_base::out);

    //Stats
    this->processed = 0;
}

/**
 * Creates a new instance of the class
 * @param fs::path path 
 * @param string familyName
 * @param unsigned int minLength
 * @param unsigned int minOcurrences
 * @param unsigned int limit
 * @param string outputFilename
 */
Txmba::Txmba(fs::path path, string familyName, unsigned int minLength, unsigned int minOcurrences, unsigned int limit, string outputFilename)
{
	//Parameters
	this->path = path;
	this->familyName = familyName;
	this->minLength = minLength;
	this->minOcurrences = minOcurrences;
	this->limit = limit;
	this->outputFilename = outputFilename;

	//Initialize file to store results
    this->outputFile.open(outputFilename, std::ios_base::app | std::ios_base::out);
    
    //Not opened proteins
    this->notopened.open("not.txt", std::ios_base::app | std::ios_base::out);

    //Stats
    this->processed = 0;
}

/**
 * Class destructor. 
 * Close all opened file handles and deallocate resources.
 */
Txmba::~Txmba()
{
	this->outputFile.close();
	this->notopened.close();
}

/**
 * Creates a new instance from the given parameters.
 * @param  int argc the quantity of arguments received
 * @param  char** argv the arguments as char*
 * @return Txmba instance
 */
Txmba Txmba::createFromParams(int argc, char* argv[])
{
	unsigned int minLength = 2;
    unsigned int minOcurrences = 1;
    unsigned int limit = 0;

	if (argc < 3) {
		throw std::runtime_error(string("Usage: ") + string(argv[0]) + string(" path familyName minLength (defaults to 2) minOcurrences (default to 1)\n"));
    }
 
    fs::path path(argv[1]);
    if(!exists(path) || !is_directory(path)) {
        throw std::runtime_error("Invalid path name");
    }

    if(argc > 3) {
        istringstream ss(argv[3]);
        if (!(ss >> minLength)) {
            throw std::runtime_error(string("Invalid minLength: ")+ string(argv[3]));
        }
    } 

    if(argc > 4) {
        istringstream ss(argv[4]);
        if (!(ss >> minOcurrences)) {
            throw std::runtime_error(string("Invalid minOcurrences: ")+ string(argv[4]));
        }
    } 

    if(argc > 5) {
        istringstream ss(argv[5]);
        if (!(ss >> limit)) {
            throw std::runtime_error(string("Invalid ocurrences: ")+ string(argv[5]));
        }
    }

    string outputFile = string(argv[1])+"-tx-mba.txt";
    if(argc > 6) {
        outputFile = string(argv[6]);
    }

    return Txmba(path, string(argv[2]), minLength, minOcurrences, limit, outputFile);
}

/**
 * Returns a string with the summary of things processed.
 * @return string
 */
string Txmba::displaySummary()
{
	return string(" >> There are ") + std::to_string(processed) + string(" tx created for ") + familyName + string(" >> ") + "\n";
}

/**
 * Return true if the limit of proteins to be processed per folder is reached.
 * @return bool
 */
bool Txmba::isLimitReached()
{
    return this->limit > 0 && this->limit == this->processed;
}

/**
 * Save the transaction made from the protein into a file.
 * @param vector<string> proteinTxData
 */
void Txmba::pushProtein(vector<string> proteinTxData)
{
    //Store family name in tx if not "-"
    if(this->familyName.compare("-") != 0) {
        proteinTxData.emplace_back(this->familyName);
    }

    //Store tx data in a file
    string tx = boost::algorithm::join(proteinTxData, ",");
    this->outputFile << tx << endl;
}

/**
 * Process a protein. In this case, for each protein, 
 * run MRs and store transaction data (each MRs in a file)
 */
void Txmba::processProtein(pair<string,string>& protein, string proteinFilename)
{
    Mrs m = Mrs::runMrs(protein.first, '+', minLength);
    vector<string> proteinTxData;
    bool shouldPush = false;
    for(auto& ocurr: *(m.getOcurrences())) {
        if(ocurr.second.size() >= this->minOcurrences) {
            proteinTxData.emplace_back(ocurr.first);
            shouldPush = true;
        }
    }

    if(shouldPush) {
        this->pushProtein(proteinTxData);
    } else {
        this->notopened << proteinFilename << endl;
    }
}

/**
 * Generates transactions for MBA as a consequence of 
 * getting into a folder and reading fasta files for proteins.
 */
void Txmba::generateTransactions()
{
	//Open folder of proteins and for each one generate a transaction
    fs::recursive_directory_iterator begin(this->path), end;
    std::vector<fs::directory_entry> files(begin, end);
    //std::vector<string> v(files.size(), ""); //Maybe better
    
    //For each file, get the proteins and process them
    for (auto& file: files) {
        string proteinFilename = file.path().generic_string();
        FastaParser f = FastaParser(proteinFilename); //Parse the protein

        for(pair<string,string>& protein: f.getProteins()) {
            this->processProtein(protein, proteinFilename);
            this->processed++;
        }

        if(this->isLimitReached()) {
            break;
        }
    }
}


////////////////////////////////////// TXMBA Bag //////////////////////////////

/**
 * Creates a new instance from the given parameters.
 * @param  int argc the quantity of arguments received
 * @param  char** argv the arguments as char*
 * @return Txmba instance
 */
TxmbaBag TxmbaBag::createFromParams(int argc, char* argv[])
{
	unsigned int minLength = 2;
    unsigned int minOcurrences = 1;
    unsigned int limit = 0;

	if (argc < 3) {
		throw std::runtime_error(string("Usage: ") + string(argv[0]) + string(" path familyName minLength (defaults to 2) minOcurrences (default to 1) limit outputFile\n"));
    }
 
    fs::path path(argv[1]);
    if(!exists(path) || !is_directory(path)) {
        throw std::runtime_error("Invalid path name");
    }

    if(argc > 3) {
        istringstream ss(argv[3]);
        if (!(ss >> minLength)) {
            throw std::runtime_error(string("Invalid minLength: ")+ string(argv[3]));
        }
    } 

    if(argc > 4) {
        istringstream ss(argv[4]);
        if (!(ss >> minOcurrences)) {
            throw std::runtime_error(string("Invalid minOcurrences: ")+ string(argv[4]));
        }
    } 

    if(argc > 5) {
        istringstream ss(argv[5]);
        if (!(ss >> limit)) {
            throw std::runtime_error(string("Invalid limit: ")+ string(argv[5]));
        }
    }

    string outputFile = string(argv[1])+"-tx-mba.txt";
    if(argc > 6) {
        outputFile = string(argv[6]);
    }

    return TxmbaBag(path, string(argv[2]), minLength, minOcurrences, limit, outputFile);
}

/**
 * Creates a new instance of the class.
 * First it joins the proteins into a single file. Then it extracts the maximal repeats for the whole bag of proteins
 * and stores it in an internal variable for further processing.
 * @param fs::path path 
 * @param string familyName
 * @param unsigned int minLength
 * @param unsigned int minOcurrences
 * @param unsigned int limit
 * @param string outputFilename
 */
TxmbaBag::TxmbaBag(fs::path path, string familyName, unsigned int minLength, unsigned int minOcurrences, unsigned int limit, string outputFilename) : Txmba(path, familyName, minLength, minOcurrences, limit, outputFilename)
{
    cout << "Joining proteins to \"" << this->path.generic_string().c_str() << "\".....";
    auto startTime = chrono::high_resolution_clock::now();
	string joinedFilename = this->joinProteinsToFile(this->path.generic_string().c_str());
    auto endTime = chrono::high_resolution_clock::now();
    cout << "...OK! (" << chrono::duration_cast<chrono::seconds>(endTime - startTime).count() << "s)" << endl;
    
    unsigned int effectiveLimit = this->limit;
    if(effectiveLimit == 0) {
        effectiveLimit = computedLimit;
    }

    //Initialize auxiliary structures
    proteinDirectory = std::vector<string>(effectiveLimit);
    proteinWithMrs = std::vector< std::list<string> >(effectiveLimit, std::list<string>());

    cout << "Proteins joined: " << effectiveLimit << endl;
    cout << "Running MRs extractor from the joined filename...." << endl;
    startTime = chrono::high_resolution_clock::now();
    this->mr = Mrs::runMrsFromFile(joinedFilename, '+', this->minLength, std::regex_replace(joinedFilename, std::regex("-joined-v2.txt"), "-runmrs.txt"));
    endTime = chrono::high_resolution_clock::now();
    cout << "    ...OK! (" << chrono::duration_cast<chrono::seconds>(endTime - startTime).count() << "s)" << endl;
}

/**
 * Generates transactions for MBA as a consequence of 
 * getting into a folder and reading fasta files for proteins.
 */
void TxmbaBag::generateTransactions()
{
    cout << endl << "Generating transactions.... " << endl;

    auto startTime = chrono::high_resolution_clock::now();
    auto endTime = chrono::high_resolution_clock::now();

    cout << "Size of proteinIndexForMrJoinedPositions: " << proteinIndexForMrJoinedPositions.size() << endl;
    cout << "Size of proteinWithMRs: " << proteinWithMrs.size() << endl;
    cout << "Size of ocurrences: " << mr.getOcurrences()->size() << endl << endl;

    int mrProcessed = 0;
    for(auto& ocurr: *(mr.getOcurrences())) {
        for(auto mrpos: ocurr.second) {
            //mrpos holds a position in the vector of ocurrences of a specified MR
            int proteinId = proteinIndexForMrJoinedPositions[mrpos];
            proteinWithMrs[proteinId].emplace_back(ocurr.first); //add to the bottom of the list
        }
        mrProcessed++;

        if(mrProcessed % 250000 == 0) {
            endTime = chrono::high_resolution_clock::now();
            cout << "Processed %" << mrProcessed  << " / " << (mr.getOcurrences())->size() << " (" << chrono::duration_cast<chrono::seconds>(endTime - startTime).count() << "s)" << endl;
            startTime = chrono::high_resolution_clock::now();
        }
    }

    cout << "Writing transactions to file..." << endl;

    for(unsigned int i = 0; i < proteinWithMrs.size(); i++) {
        if(proteinWithMrs[i].size() > 0) {
            proteinWithMrs[i].unique();
            if(familyName != "-") {
                this->outputFile << "Fam=" << familyName << ",";
            }
            this->outputFile << boost::algorithm::join(proteinWithMrs[i], ",") << endl;
            processed++;
        }

        if(i % 1000 == 0) {
            cout << i << "th transaction written to file" << endl;
        }
    }
    cout << "DONE!" << endl;
}

/**
 * Process a protein. In this case, 
 * for each protein get the bag computed MRs for the protein and mark the ones that belong
 * to the current protein and push the transaction data.
 */
void TxmbaBag::processProtein(pair<string,string>& protein, string proteinFilename)
{
/*
    vector<string> proteinTxData;
    bool shouldPush = false;

    for(auto& ocurr: *(this->mr.getOcurrences())) {
        if(ocurr.first.length() >= this->minLength && protein.first.find(ocurr.first) != string::npos && ocurr.second.size() >= this->minOcurrences) {
            proteinTxData.emplace_back(ocurr.first);
            shouldPush = true;
        }
    }
    
    if(shouldPush) {
        this->pushProtein(proteinTxData);
    } else {
        this->notopened << proteinFilename << endl;
    }
*/
}

/**
 * Class destructor. 
 * Close all opened file handles and deallocate resources.
 */
TxmbaBag::~TxmbaBag()
{
    this->outputFile.close();
    this->notopened.close();
}

/**
 * Joins proteins form a path to a file. It appends the suffix "-joined" to the output file.
 * @param  const char* filePath
 * @return string the pathname of the joined file.
 */
string TxmbaBag::joinProteinsToFile(const char* filePath)
{
    fs::path path(filePath);
    if(!exists(path) || !is_directory(path)) {
        throw new std::exception();
    }

    string pathQueried = Mrs::cleanPath(path);
    string joinedFilename = pathQueried+"-joined-v2.txt";

    fs::path joinedPath(joinedFilename);
        
    //If no joined file exists, get all the proteins from folder, parse and joined them into a file.
    fs::recursive_directory_iterator begin(path), end;
    std::vector<fs::directory_entry> files(begin, end);

    std::vector<string> proteinTextVector;
    int pushed = 0;

    for(auto& file: files) {
        FastaParser f = FastaParser(file.path().generic_string());
        for(auto& proteinAndComment: f.getProteins()) {
            proteinTextVector.emplace_back(proteinAndComment.first); //fill aux structures
            this->proteinDirectory.emplace_back(proteinAndComment.first);
            pushed++;
        }
    }

    //update limit variable in case it was not supplied
    if(limit == 0) {
        computedLimit = pushed;
    }

    //cout << "There are " << pushed << " proteins loaded." << endl;
    string joined = boost::algorithm::join(proteinTextVector,"+");

    //Set the protein index
    proteinIndexForMrJoinedPositions = std::vector<int>(joined.length(), (-1));

    int index = 0;
    for(unsigned int i = 0; i < proteinDirectory.size(); i++) {
        for(unsigned int j = 0; j < proteinDirectory[i].length(); j++) {
            proteinIndexForMrJoinedPositions[index] = i;
            index++;
        }
        index++; //Exclude the "+"
    }

    ofstream joinedFile;
    joinedFile.open(joinedFilename);
    joinedFile << joined;
    joinedFile.close();

    return joinedFilename;
}