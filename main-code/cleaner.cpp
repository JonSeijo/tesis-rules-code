#include <cstdlib>
#include "txmba_cleaner.h"

void printHelp()
{
	cout << " Help: " << endl;
	cout << "./cleaner input mode output" << endl << endl;
	cout << "mode is 0 for inclusion cleaning, 1 for exclusion " << endl;
}

int main(int argc, char* argv[])
{
	bool mode;
	
	if(argc < 4) {
		cerr << "** Error not enough parameters! " << endl;
		printHelp();
		return EXIT_FAILURE;
	}

	string input = string(argv[1]);
	string output = string(argv[3]);

    istringstream ss(argv[2]);
    if (!(ss >> mode)) {
    	cerr << "** Invalid mode! " << endl;
		return EXIT_FAILURE;
    }

    
    TxmbaCleaner cleaner = TxmbaCleaner(input, mode, output);
    cleaner.cleanLines();

    return EXIT_SUCCESS;
}
