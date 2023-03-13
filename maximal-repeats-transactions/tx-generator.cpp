#include <iostream>
#include <algorithm>
#include <iterator>
#include <math.h>
#include  "txmers.h"




bool fileInitialization(ofstream& osData, const string suffix, const string outputFilename){
    string filenameToOpen = outputFilename+"_"+suffix+".csv";
    osData.open(filenameToOpen.c_str(), std::ofstream::trunc); // std::ofstream::trunc to clear the output file
    if(!osData.good()){
        cout << "Error! function " << __FUNCTION__ << " cannot open " << filenameToOpen << endl;
        return false;
    }


    return true;
}    

void saveFile(ofstream& os, map<unsigned int, set<string> >& txs){
         // for each tx
         for (std::map<unsigned int,set<string> >::iterator it_tx=txs.begin(); it_tx!=txs.end(); ++it_tx){
            //for each item (mr) 
            for (std::set<string>::iterator it_item = (it_tx->second).begin(); it_item != (it_tx->second).end(); ++it_item){
                if(it_item != (it_tx->second).begin()) os << ",";
                os << *it_item;        
            }
            os << endl;
         }
}

void addMrs(map<uint, set<string> >& toAddMrs, map<uint, set<string> >& totalMrs) {
    for (auto &kv : toAddMrs) {
        uint proteinId = kv.first;
        set<string> mrs = kv.second;
        totalMrs[proteinId].insert(mrs.begin(), mrs.end());
    }
}

int main(int argc, const char *argv[]) {
  

    // paramaeter checking
    if((argc!=4) && (argc!=7)){
                cout<<"usage example: " << argv[0] << " familyName familyDatasetFolder outputFilename minLengthOfPattern maxLengthOfPattern minNumberOfAffectedProteins" << endl;
                return 0;
    }

    bool ok;

    // 1. Parameters
    // =============
    //a. familyName
    string familyName   =  argv[1];

    //a. familyDatasetFolder
    string familyDatasetFolder   =  argv[2];

    //b. outputFilename
    string outputFilename = argv[3];
    
    unsigned int minLengthOfPattern=0; 
    unsigned int maxLengthOfPattern=999999999; 
    unsigned int minNumberOfAffectedProteins=0;
    if(argc==7){
        minLengthOfPattern = (unsigned int)Tools::toInt(argv[4]);
        maxLengthOfPattern = (unsigned int)Tools::toInt(argv[5]);
        minNumberOfAffectedProteins = (unsigned int)Tools::toInt(argv[6]);
    }
  
//     vector<string> fsFolderNames=familiesFolderNames();
  
    cout << endl << endl << endl; 
    cout << "Parameters" << endl;
    cout << "==========" << endl;
    cout << " 1. familyName                  : " << familyName << endl;
    cout << " 2. familyDatasetFolder         : " << familyDatasetFolder << endl;
    cout << " 3. outputFilename              : " << outputFilename << endl;
    cout << " 4. minLengthOfPattern          : " << minLengthOfPattern << endl;
    cout << " 5. maxLengthOfPattern          : " << maxLengthOfPattern << endl;
    cout << " 6. minNumberOfAffectedProteins : " << minNumberOfAffectedProteins << endl;
    cout << endl << endl;
    
    // 2. Outputdata file Initialization
    // =================================
    //
    
    
    ofstream smr_osData;
    ofstream  nn_osData;
    ofstream  ne_osData;
    ofstream  all_osData;


    ok=fileInitialization(smr_osData,"SMR", outputFilename);
    if(!ok) return false;
    ok=fileInitialization( nn_osData, "NN", outputFilename);
    if(!ok) return false;
    ok=fileInitialization( ne_osData, "NE", outputFilename);
    if(!ok) return false;
    ok=fileInitialization( all_osData, "ALL", outputFilename);
    if(!ok) return false;
    

    // 3. MER sets Computation
    // =================================
    //
    // ... TX-MERs Computation
    txmers txmersSets(familyDatasetFolder, familyName, minLengthOfPattern, maxLengthOfPattern, minNumberOfAffectedProteins);
    
    std::cout << "Se calcularon " << txmersSets.NN_txs.size() << " nn txs" << endl;

    saveFile(smr_osData,txmersSets.SMR_txs);
    saveFile( nn_osData,txmersSets.NN_txs);
    saveFile( ne_osData,txmersSets.NE_txs);
    
    smr_osData.close();
    nn_osData.close();
    ne_osData.close();


    // Union de todos los MR de tipo NN, NE y SMR para cada proteina. Lo guardo en concat_mrs
    map<uint, set<string> > concat_mrs;
    addMrs(txmersSets.NN_txs, concat_mrs);
    addMrs(txmersSets.NE_txs, concat_mrs);
    addMrs(txmersSets.SMR_txs, concat_mrs);
    saveFile( all_osData, concat_mrs);
    all_osData.close();



//         int cantTx = 3;
//         cout << "SMRs" << endl;    
//         for(unsigned int iTx=0;iTx<cantTx;iTx++){
//             set<string> s=merSet.SMR_txs[iTx];
//             cout << "Tx " << iTx << ": ";
//             std::set<string>::iterator it;
//             for (it = s.begin(); it != s.end(); ++it){
//                     cout << *it << ","; // Note the "*" here
//                 
//             }
//             cout << endl;
//             
//         }
// 
//         cout << "NNs" << endl;    
//         for(unsigned int iTx=0;iTx<cantTx;iTx++){
//             set<string> s=merSet.NN_txs[iTx];
//             cout << "Tx " << iTx << ": ";
//             std::set<string>::iterator it;
//             for (it = s.begin(); it != s.end(); ++it){
//                     cout << *it << ","; // Note the "*" here
//                 
//             }
//             cout << endl;
//             
//         }
// 
//         cout << "NEs" << endl;    
//         for(unsigned int iTx=0;iTx<cantTx;iTx++){
//             set<string> s=merSet.NE_txs[iTx];
//             cout << "Tx " << iTx << ": ";
//             std::set<string>::iterator it;
//             for (it = s.begin(); it != s.end(); ++it){
//                     cout << *it << ","; // Note the "*" here
//                 
//             }
//             cout << endl;
//             
//         }
//         
// //         smr_osData << fsFolderNames[iFamily] << "," << merSet.numberOfProteinsInFamily << "," << merSet.numberOfAminoacidsInFamily;
// //          nn_osData << fsFolderNames[iFamily] << "," << merSet.numberOfProteinsInFamily << "," << merSet.numberOfAminoacidsInFamily;
// //          ne_osData << fsFolderNames[iFamily] << "," << merSet.numberOfProteinsInFamily << "," << merSet.numberOfAminoacidsInFamily;
// //         
// //         for(unsigned int lengthOfPattern=minLengthOfPattern;lengthOfPattern<=maxLengthOfPattern;lengthOfPattern++){
// //             unsigned int smrCounter=getNumberOfElements(merSet.taillefer_patterns_SMR         ,lengthOfPattern);
// //             unsigned int  nnCounter=getNumberOfElements(merSet.taillefer_patterns_MR_nonNested,lengthOfPattern);
// //             unsigned int  neCounter=getNumberOfElements(merSet.taillefer_patterns_MR_nested   ,lengthOfPattern);
// // //             unsigned int totalMers=smrCounter+nnCounter+neCounter;
// //             smr_osData << "," << smrCounter;
// //              nn_osData << "," << nnCounter;
// //              ne_osData << "," << neCounter;
// //         }
// //         smr_osData << endl;
// //          nn_osData << endl;
// //          ne_osData << endl;
// // 
// //     smr_osData.close();
// //      nn_osData.close();
// //      ne_osData.close();
// //     
// 
  
    return 0;

  
}


