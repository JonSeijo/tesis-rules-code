#!/bin/bash
BASEDIR="../../data/proteins/familyDataset"
#BASEDIR="../../data/proteins/testGroupDataset"
PARAMS="4 1 38051 ank-mr-protein-4.txt"



#./txmba_bag ../../data/proteins/familyDataset/ank/ - 4 1 38000 ank-mr-bag-4.txt

#./txmba $BASEDIR/ABCtran/ ABCtran $PARAMS
#./txmba $BASEDIR/Collagen/ Collagen $PARAMS
#./txmba $BASEDIR/GDCP/ GDCP $PARAMS
#./txmba $BASEDIR/HemolysinCabind/ HemolysinCabind $PARAMS
#./txmba_bag $BASEDIR/MgtE/ MgtE $PARAMS
#./txmba $BASEDIR/MORN/ MORN $PARAMS
#./txmba $BASEDIR/Pentapeptide/ Pentapeptide $PARAMS
#./txmba $BASEDIR/PPR/ PPR $PARAMS
#./txmba $BASEDIR/Thaumatin/ Thaumatin $PARAMS
#./txmba $BASEDIR/YadAhead/ YadAhead $PARAMS
./txmba_each $BASEDIR/ank/ - $PARAMS

#./txmba_bag $BASEDIR/PUD/ PUD $PARAMS
#./txmba $BASEDIR/CorA/ CorA $PARAMS
#./txmba $BASEDIR/Globin/ Globin $PARAMS
#./txmba $BASEDIR/Hexapep/ Hexapep $PARAMS
#./txmba $BASEDIR/MIP/ MIP $PARAMS
#./txmba_bag $BASEDIR/Nebulin/ Nebulin $PARAMS
#./txmba $BASEDIR/PeptidaseC25/ PeptidaseC25 $PARAMS
#./txmba $BASEDIR/TPR1/ TPR1 $PARAMS
#./txmba $BASEDIR/CWbinding1/ CWbinding1 $PARAMS
#./txmba $BASEDIR/Glycohydro19/ Glycohydro19 $PARAMS
#./txmba $BASEDIR/Kelch1/ Kelch1 $PARAMS
#./txmba $BASEDIR/Mitocarr/ Mitocarr $PARAMS
#./txmba $BASEDIR/NEWAnk/ NEWAnk $PARAMS
#./txmba $BASEDIR/PFLlike/ PFLlike $PARAMS
#./txmba $BASEDIR/PUF/ PUF $PARAMS
#./txmba $BASEDIR/TSP1/ TSP1 $PARAMS
#./txmba_bag $BASEDIR/Annexin/ Annexin $PARAMS
#./txmba $BASEDIR/dehalogenase/ dehalogenase $PARAMS
#./txmba $BASEDIR/GreAGreB/ GreAGreB $PARAMS
#./txmba $BASEDIR/Ldlrecepta/ Ldlrecepta $PARAMS
#./txmba_bag $BASEDIR/mix/ mix $PARAMS
#./txmba $BASEDIR/NEWWD40/ NEWWD40 $PARAMS
#./txmba $BASEDIR/PIN/ PIN $PARAMS
#./txmba $BASEDIR/Rhomboid/ Rhomboid $PARAMS
#./txmba $BASEDIR/ValtRNAsyntC/ ValtRNAsyntC $PARAMS
#./txmba $BASEDIR/Arm/ Arm $PARAMS
#./txmba $BASEDIR/Fer4/ Fer4 $PARAMS
#./txmba $BASEDIR/HEAT/ HEAT $PARAMS
#./txmba $BASEDIR/Ldlreceptb/ Ldlreceptb $PARAMS
#./txmba_bag $BASEDIR/mixScrambled/ mixScrambled $PARAMS
#./txmba $BASEDIR/PBP/ PBP $PARAMS
#./txmba $BASEDIR/Pkinase/ Pkinase $PARAMS
#./txmba $BASEDIR/Sel1/ Sel1 $PARAMS
#./txmba $BASEDIR/wd/ wd $PARAMS
#./txmba $BASEDIR/Filamin/ Filamin $PARAMS
#./txmba $BASEDIR/HelicaseC/ HelicaseC $PARAMS
#./txmba $BASEDIR/LRR1/ LRR1 $PARAMS
#./txmba $BASEDIR/mixUniformDistributed/ mixUniformDistributed $PARAMS
#./txmba $BASEDIR/PD40/ PD40 $PARAMS
#./txmba $BASEDIR/PPbinding/ PPbinding $PARAMS
#./txmba $BASEDIR/TerB/ TerB $PARAMS
