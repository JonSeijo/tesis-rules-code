#include "scrambler.h"

/**
 * The available aminoacids code
 * @var const char
 */
const char Scrambler::aminoAcids[] = {'A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y'};

/**
 * From a string generate a path (boost) path object
 * @param  string dir 
 * @return fs::path
 */
fs::path Scrambler::createPathObject(string dir)
{
    fs::path path(dir.c_str());
    if(!exists(path) || !is_directory(path)) {
        throw std::runtime_error("Invalid path name");
    }

    return path;
}

/**
 * Creates a new instance of the class
 * @param string the input file for fetching the proteins
 * @param string the output file for saving the generated proteins 
 */
Scrambler::Scrambler(string input, string output)
{
    this->inputDirectory = this->createPathObject(input);
    this->outputDirectory = output;
}

/**
 * Scrambles generates a random_shuffle (see STL docs) 
 * of the input
 * @param  string input the input to shuffle
 * @return string the shuffled input
 */
string Scrambler::scramble(string input)
{
    random_shuffle(input.begin(), input.end());
    return input;
}

/**
 * Generates data of the given length taken from a uniform distribution of a specified
 * aminoacid dataset
 * @param  int length
 * @return string the uniform-generated data
 */
string Scrambler::uniform(int length)
{
    string output;
    for(int i = 0; i < length; i++) {
        output.append(1, Scrambler::aminoAcids[getRandomAminoAcidCode()]);
    }
    return output;
}

/**
 * Generates an integer from a random distribution to be used as an index for fetching an aminoacid 
 * from the table
 * @return int
 */
int Scrambler::getRandomAminoAcidCode()
{
    std::random_device randomDevice;  //Will be used to obtain a seed for the random number engine
    std::mt19937 generator(randomDevice()); //Standard mersenne_twister_engine seeded with rd()
    std::uniform_int_distribution<> uniformDist(0, AMINO_ACID_COUNT-1);
    return uniformDist(generator);
}

/**
 * Replaces an ocurrence with another in a string passed as parameter. Returns true if the
 * replacement was successfull
 * @param  string& str the string to be replace
 * @param  const string& from the string to search for replacement
 * @param  const string& to the string to be used as a replacement
 * @return bool whether the replacement was successfull
 */
bool Scrambler::replace(string& str, const string& from, const string& to)
{
    size_t start_pos = str.find(from);
    if(start_pos == std::string::npos)
        return false;
    str.replace(start_pos, from.length(), to);
    return true;
}

/**
 * Trasverse the filesystem and generate the corresponding protein combinations
 * @param  int mode of the replacement function (uniform vs scrambled)
 */
void Scrambler::generateVariations(int mode)
{
	//Open folder of proteins and for each one generate a transaction
    fs::recursive_directory_iterator begin(this->inputDirectory), end;
    std::vector<fs::directory_entry> files(begin, end);
    
    //For each file, get the proteins and process them
    for (auto& file: files) {
        string operationMode;
        string proteinFilename = file.path().generic_string();
        FastaParser f = FastaParser(proteinFilename); //Parse the protein
        
        //Select the operation mode
        if(mode == MODE_SCRAMBLE) {
            operationMode = "scramble";
        } else {
            operationMode = "uniform";
        }

        //Generate the filename based on the input and output routes
        string outputFilename = proteinFilename;
        string suffix = "-"+operationMode+".fasta";
        
        this->replace(outputFilename, this->inputDirectory.generic_string(), this->outputDirectory);
        if(outputFilename.find(".fasta") != string::npos) {
            this->replace(outputFilename, string(".fasta"), suffix);
        }

        ofstream out;
        out.open(outputFilename, std::ios_base::out);
        for(ProteinAndComment& pc: f.getProteins()) {
            if(pc.second.length() > 0) {
                out << pc.second << endl;
            }

            string processed;
            if(mode == MODE_SCRAMBLE) {
                processed = scramble(pc.first);
            } else {
                processed = uniform(pc.first.length());
            }
            out << processed << endl;
        }
        out.close();
    }
}
