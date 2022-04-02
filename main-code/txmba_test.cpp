#include <cppunit/ui/text/TestRunner.h>
#include <cppunit/extensions/HelperMacros.h>
#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/BriefTestProgressListener.h>
#include <cppunit/CompilerOutputter.h>
#include <cppunit/TextOutputter.h>
#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/TestResult.h>
#include <cppunit/TestRunner.h>
#include <cppunit/TestResultCollector.h>
#include "parse.h"
#include "protein.h"
#include "txmba.h"
#include <iostream>
#include <exception>

class TxmbaTest : public CppUnit::TestFixture
{

    private:
        CPPUNIT_TEST_SUITE( TxmbaTest );
        
/*
        */
        CPPUNIT_TEST( testSigleTransactionOkForMrForEachProtein );
        CPPUNIT_TEST( testInvalidPathThrowsException );
        CPPUNIT_TEST( testOverrideConstructorWithInfoIsRetreivedOk );
        CPPUNIT_TEST( testGeneratorAreEqualOnOneProtein );
        CPPUNIT_TEST( testGeneratorEachForTwoProteins1 );
        CPPUNIT_TEST( testGeneratorEachForTwoProteins2 );
        CPPUNIT_TEST( testGeneratorBagForTwoProteins1 );
        CPPUNIT_TEST( testGeneratorBagForTwoProteins2 );

        CPPUNIT_TEST_SUITE_END();

    public:
        void setUp() {}

        void tearDown() {}

        void testSigleTransactionOkForMrForEachProtein()
        {
            string expected = "AA,ADVNA,AE,AN,DK,DL,ED,EI,EV,EVLLKY,FG,GADVNA,GHLEI,GHLEIVEVLLKYGADVNA,GK,HL,IL,LA,LE,LL,NG,QD,SD,TPLHL,TPLHLAA,VN";
            string out = "tests/txs/1/out/1-tx-test-out.txt";
            writeOutputToFile(out, "");
            fs::path path("tests/txs/1/in");
            Txmba txGenerator = Txmba(path, "-", 2, 1, 0, out);
            txGenerator.generateTransactions();
            string result = readFileIntoString(out);

            CPPUNIT_ASSERT_EQUAL(expected, result);
        }

        void testInvalidPathThrowsException()
        {
            char *argv[6] = {"tests/txs/1/asdfasdfasdfsdafsdf", "-", "2", "1", "0", "testssdfasd"};
            int argc = 6;
            CPPUNIT_ASSERT_THROW_MESSAGE("Invalid path name", Txmba::createFromParams(argc, argv), std::runtime_error);
        }

        void testOverrideConstructorWithInfoIsRetreivedOk()
        {
            string out = "tests/txs/1-tx-test-out.txt";
            fs::path path("tests/txs/1/");
            TxmbaBag txGenerator = TxmbaBag(path, "-", 2, 1, 0, out);

            unsigned int l = txGenerator.minLength;
            unsigned int mo = txGenerator.minOcurrences;
            unsigned int li = txGenerator.limit;

            CPPUNIT_ASSERT_EQUAL(string("-"), txGenerator.familyName);
            CPPUNIT_ASSERT_EQUAL((unsigned int)2, l);
            CPPUNIT_ASSERT_EQUAL((unsigned int)1, mo);
            CPPUNIT_ASSERT_EQUAL((unsigned int)0, li);
        }

        void testGeneratorAreEqualOnOneProtein()
        {
            fs::path path("tests/txs/2/in");
            string out = "tests/txs/2/out/each-out.txt";
            Txmba txGenerator = Txmba(path, "-", 2, 1, 0, out);
            txGenerator.generateTransactions();
            string result = readFileIntoString(out);

            string out2 = "tests/txs/2/out/bag-out.txt";
            TxmbaBag txGeneratorBag = TxmbaBag(path, "-", 2, 1, 0, out2);
            txGeneratorBag.generateTransactions();
            string expected = readFileIntoString(out);

            CPPUNIT_ASSERT_EQUAL(expected, result);
        }


        void testGeneratorEachForTwoProteins1()
        {
            fs::path path("tests/txs/3/in");
            string out = "tests/txs/3/out/each-result.txt";
            writeOutputToFile(out, "");
            Txmba txGeneratorEach = Txmba(path, "-", 2, 1, 0, out);
            txGeneratorEach.generateTransactions();
            string result = readFileIntoString(out);
            string expected = readFileIntoString("tests/txs/3/out/each-expected.txt");
            CPPUNIT_ASSERT_EQUAL(expected, result);
        }

        void testGeneratorEachForTwoProteins2()
        {
            fs::path path("tests/txs/4/in");
            string out = "tests/txs/4/out/each-result.txt";
            writeOutputToFile(out, "");
            Txmba txGeneratorEach = Txmba(path, "-", 2, 1, 0, out);
            txGeneratorEach.generateTransactions();
            string result = readFileIntoString(out);
            string expected = readFileIntoString("tests/txs/4/out/each-expected.txt");
            CPPUNIT_ASSERT_EQUAL(expected, result);
        }

        void testGeneratorBagForTwoProteins1()
        {
            fs::path path("tests/txs/3/in");
            string out = "tests/txs/3/out/bag-result.txt";
            writeOutputToFile(out, "");
            TxmbaBag txGeneratorBag = TxmbaBag(path, "-", 2, 1, 0, out);
            txGeneratorBag.generateTransactions();
            string result = readFileIntoString(out);
            string expected = readFileIntoString("tests/txs/3/out/bag-expected.txt");
            CPPUNIT_ASSERT_EQUAL(expected, result);
        }


        void testGeneratorBagForTwoProteins2()
        {
            fs::path path("tests/txs/4/in");
            string out = "tests/txs/4/out/bag-result.txt";
            writeOutputToFile(out, "");
            TxmbaBag txGeneratorBag = TxmbaBag(path, "-", 2, 1, 0, out);
            txGeneratorBag.generateTransactions();
            string result = readFileIntoString(out);
            string expected = readFileIntoString("tests/txs/4/out/bag-expected.txt");
            CPPUNIT_ASSERT_EQUAL(expected, result);
        }


        //Utility functions
        string readFileIntoString(string filename)
        {
            string content = string();
            std::ifstream infile(filename.c_str(), std::ifstream::in);
            std::string line;

            //Get length of file
            infile.seekg (0, infile.end);
            int length = infile.tellg();
            infile.seekg (0, infile.beg);

            if(length > 0) {
                while (std::getline(infile, line)) {
                    std::istringstream iss(line);
                    string currentLine = iss.str();

                    if(currentLine.length()>0) {
                        content = content + currentLine;
                    }
                }
            }

            //Push last item read to internal data structures
            content.erase(std::remove(content.begin(), content.end(), '\n'), content.end());
            infile.close();
            return content;
        }

        void writeOutputToFile(string path, string data)
        {
            ofstream out;
            out.open(path);
            out << data;
            out.close();
        }

};

CPPUNIT_TEST_SUITE_REGISTRATION( TxmbaTest );

int main(int argc, char** argv)
{
    // Create the event manager and test controller
    CppUnit::TestResult controller;
    // Add a listener that colllects test result
    CppUnit::TestResultCollector result;
    controller.addListener( &result );
    // Add a listener that print dots as test run.
    CppUnit::BriefTestProgressListener progress;
    controller.addListener( &progress );

    CppUnit::TextUi::TestRunner runner;
    CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry();
    runner.addTest( registry.makeTest() );
    std::cout << std::endl << " ====== Running Tests ======" << std::endl;
    runner.run(controller);
    // Print test in a compiler compatible format.
    std::cout << std::endl << " ====== Test Results ======" << std::endl;
    CppUnit::CompilerOutputter outputter( &result, CppUnit::stdCOut() );
    //CppUnit::TextOutputter outputter( &result, CppUnit::stdCOut() );
    outputter.write();

    return result.wasSuccessful() ? 0 : 1;
}