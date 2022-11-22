#include "scrambler.h"

int main(int argc, char* argv[])
{
	string input;
	string output;
	int mode;
	int retCode = 0;
	
	if(argc == 4) {
        istringstream ss(argv[3]);
        if ((!(ss >> mode)) || (mode != MODE_UNIFORM && mode != MODE_SCRAMBLE)) {
            throw std::runtime_error(string("Invalid mode!"));
        }

        input = string(argv[1]);
        output = string(argv[2]);
		
		Scrambler s = Scrambler(input, output);
		s.generateVariations(mode);
    } else {
    	retCode = 1;
    	std::cerr << "Help! - ./scrambler_app input output mode (1 scramble, 2 uniform)" << endl;
    }

    
    return retCode;
}
