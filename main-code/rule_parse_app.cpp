#include "rule_parse_and_match.h"

int main(int argc, char* argv[])
{
	string ruleFile;
	string proteinDirectory;
	string outDirectory;
	int retCode = 0;
	
	if(argc == 4) {
        ruleFile = string(argv[1]);
        proteinDirectory = string(argv[2]);
        outDirectory = string(argv[3]);
		
		RuleParser rp = RuleParser(ruleFile, proteinDirectory, outDirectory);
        rp.processRuleFile(); 
    } else {
    	retCode = 1;
    	std::cerr << "Help! - ./rule_parser_app ruleFile proteinDirectory outDirectory" << endl;
    }

    
    return retCode;
}