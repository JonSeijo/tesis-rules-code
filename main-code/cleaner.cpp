#include <cstdlib>
#include "txmba_cleaner.h"

void printHelp()
{
	cout << " Help: " << endl;
	cout << "./cleaner input mode output" << endl << endl;
	cout << "mode is: " << endl
		 << " 0 for exclusion cleaning (substring), " << endl
		 << " 1 for inclusion (superstring) " << endl
		 << " 2 for min_len (exact) " << endl;
}

int main(int argc, char* argv[])
{
	int mode;
	
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

    auto cleanMode = static_cast<CleanMode>(mode);
    TxmbaCleaner cleaner = TxmbaCleaner(input, cleanMode, output);
    cleaner.cleanLines();

    return EXIT_SUCCESS;
}
