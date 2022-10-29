.PHONY= clean clean_all build
CXX=g++
CXXFLAGS=-O2 -Wall -std=c++11		## flags del compilador: Wall para "warnings all"
OBJ=parse.o
LIBSCPPUNIT = -lcppunit -I .
TESTEXEC=parse_test mrs_test txmba_test
MAINEXEC=parse
ODIR=.
_DEPS= parser.h protein.h
BOOSTFS=-lboost_filesystem -lboost_system
DEPS = $(_DEPS)

$(ODIR)/%.o: %.cpp $(DEPS)
	$(CXX) -c -o $@ $< $(CXXFLAGS)

all: all_main all_tests

all_main: parse coverage db cleaner txmba_each txmba_bag freq_dist rule_parse_app scrambler_app

protein:
	$(CXX) -c protein.cpp -o protein.o $(CXXFLAGS) $(BOOSTFS)

parse: protein
	$(CXX) -c parse.cpp -o parse.o $(CXXFLAGS) $(BOOSTFS)

coverage: parse
	$(CXX) compute_coverage_family.cpp parse.o -o ccf $(BOOSTFS) $(CXXFLAGS)

db: parse
	$(CXX) create_db.cpp parse.o -o db $(BOOSTFS) -lsqlite3 $(CXXFLAGS) -O2

txmba: parse
	$(CXX) -c txmba.cpp -o txmba.o $(BOOSTFS) $(CXXFLAGS) -O2
	#$(CXX) create_tx_for_mba.cpp parse.o -o txmba_orig $(BOOSTFS) $(CXXFLAGS) -O2

txmba_cleaner: parse
	$(CXX) -c txmba_cleaner.cpp -o txmba_cleaner.o $(BOOSTFS) $(CXXFLAGS) -O2

cleaner: txmba_cleaner
	$(CXX) cleaner.cpp txmba_cleaner.o -o cleaner $(BOOSTFS) $(CXXFLAGS) -O2


txmba_each: txmba
	$(CXX) txmba_each.cpp parse.o protein.o txmba.o -o txmba_each $(CXXFLAGS) $(BOOSTFS)

txmba_bag: txmba
	$(CXX) txmba_bag.cpp parse.o protein.o txmba.o -o txmba_bag $(CXXFLAGS) $(BOOSTFS)

freq_dist: protein parse
	$(CXX) calculate_freq_dist_for_family.cpp protein.o parse.o -o freq_dist $(BOOSTFS) $(CXXFLAGS) -O2

rule_parse: parse txmba
	$(CXX) -c rule_parse_and_match.cpp parse.o protein.o txmba.o -o rule_parse_and_match.o $(CXXFLAGS) $(BOOSTFS) -O2

rule_parse_app: rule_parse
	$(CXX) rule_parse_app.cpp rule_parse_and_match.o protein.o parse.o -o rule_parse_app $(CXXFLAGS) $(BOOSTFS)

scrambler: parse
	$(CXX) -c scrambler.cpp -o scrambler.o $(CXXFLAGS) $(BOOSTFS) -O2

scrambler_app: scrambler
	$(CXX) scrambler_app.cpp scrambler.o parse.o -o scrambler_app $(CXXFLAGS) $(BOOSTFS)

## Tests
all_tests: test txmba_test txmba_cleaner_test rule_parse_test scrambler_test

test: protein parse
	$(CXX) parse_test.cpp parse.o protein.o -o parse_test $(CXXFLAGS) $(LIBSCPPUNIT) $(BOOSTFS)
	$(CXX) mrs_test.cpp parse.o protein.o -o mrs_test $(CXXFLAGS) $(LIBSCPPUNIT) $(BOOSTFS)

txmba_test: txmba cleaner
	$(CXX) txmba_test.cpp parse.o protein.o txmba.o -o txmba_test $(CXXFLAGS) $(LIBSCPPUNIT) $(BOOSTFS)

txmba_cleaner_test: cleaner txmba_cleaner txmba
	$(CXX) txmba_cleaner_test.cpp parse.o protein.o txmba.o txmba_cleaner.o -o txmba_cleaner_test $(CXXFLAGS) $(LIBSCPPUNIT) $(BOOSTFS)

rule_parse_test: rule_parse
	$(CXX) rule_parse_test.cpp parse.o protein.o txmba.o rule_parse_and_match.o -o rule_parse_test $(CXXFLAGS) $(LIBSCPPUNIT) $(BOOSTFS)

scrambler_test: scrambler
	$(CXX) scrambler_test.cpp parse.o scrambler.o -o scrambler_test $(CXXFLAGS) $(LIBSCPPUNIT) $(BOOSTFS)

build: clean
	parse
	parse_test

clean_tests:
	rm -f $(TESTEXEC)
	rm -f "tests/txs/1/out/1-tx-test-out.txt"
	rm -f "tests/txs/2/out/bag-out.txt"
	rm -f "tests/txs/2/out/each-out.txt"
	rm -f "tests/txs/3/out/bag-result.txt"
	rm -f "tests/txs/3/out/each-result.txt"
	rm -f "tests/txs/4/out/each-result.txt"
	rm -f "tests/txs/4/out/bag-result.txt"
	rm -f "tests/cleaner_tests/tx1.inclusion.result2.txt"
	rm -f "tests/cleaner_tests/tx1.exclusion.result2.txt"
	rm -f "tests/cleaner_tests/tx1.inclusion.result.txt"
	rm -f "tests/cleaner_tests/tx1.exclusion.result.txt"
	rm -f "tests/cleaner_tests/tx1.minimum.result.txt"
	rm -f "tests/cleaner_tests/tx1.minimum.result2.txt"

clean:
	rm -f $(ODIR)/*.o
	
clean_all: clean clean_tests
	rm -f $(MAINEXEC)

.PHONY: clean