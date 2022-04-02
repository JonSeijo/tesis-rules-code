#include "txmba.h"

int main(int argc, char* argv[])
{
    try {
    	TxmbaBag txGenerator = TxmbaBag::createFromParams(argc, argv);
    	txGenerator.generateTransactions();
    	cout << txGenerator.displaySummary();
    } catch(std::runtime_error e) {
    	cout << "** Error: " << e.what() << endl;
    }
    
    return 0;
}
