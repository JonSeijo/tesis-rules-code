#include "txmba.h"

int main(int argc, char* argv[])
{
    try {
    	Txmba txGenerator = Txmba::createFromParams(argc, argv);	
    	txGenerator.generateTransactions();
    	cout << txGenerator.displaySummary();
    } catch(std::runtime_error e) {
    	cout << "** Error: " << e.what() << endl;
    }
    
    return 0;
}
