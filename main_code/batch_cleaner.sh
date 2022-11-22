#!/bin/bash
BASEDIR="resultados/experimento6/"

printf "Inclusion bag...\n"
./cleaner $BASEDIR/ank-scrambled-mr4.txt 1 $BASEDIR/ank-scrambled-mr4-inclusion.txt
./cleaner $BASEDIR/ank-uniform-mr4.txt 1 $BASEDIR/ank-uniform-mr4-inclusion.txt

printf "Exclusion bag...\n"
./cleaner $BASEDIR/ank-scrambled-mr4.txt 0 $BASEDIR/ank-scrambled-mr4-exclusion.txt
./cleaner $BASEDIR/ank-uniform-mr4.txt 0 $BASEDIR/ank-uniform-mr4-exclusion.txt

printf "Done!\n"
