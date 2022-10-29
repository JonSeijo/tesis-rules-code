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
#include <iostream>
#include <exception>
#include <boost/algorithm/string/trim.hpp>
#include "parse.h"
#include "protein.h"
#include "txmba.h"
#include "txmba_cleaner.h"

class TxmbaCleanerTest : public CppUnit::TestFixture
{

    private:
        CPPUNIT_TEST_SUITE( TxmbaCleanerTest );
        CPPUNIT_TEST( testFind );
        CPPUNIT_TEST( testCleanLineInclusion1 );
        CPPUNIT_TEST( testCleanLineInclusion2 );
        CPPUNIT_TEST( testCleanLineExclusion1 );
        CPPUNIT_TEST( testFileCleanerExclusion );
        CPPUNIT_TEST( testFileCleanerInclusion );

        CPPUNIT_TEST_SUITE_END();

    public:
        void setUp() {}

        void tearDown() {}

        void testFind()
        {
            size_t pos = 1;
            CPPUNIT_ASSERT_EQUAL(string::npos, string("AV").find(string("AAV")));
            CPPUNIT_ASSERT_EQUAL(pos, string("AAV").find(string("AV")));
        }

        void testCleanLineInclusion1()
        {
            TxmbaCleaner cleaner = TxmbaCleaner("a", CleanMode::superstring, "b");
            CPPUNIT_ASSERT_EQUAL(string("AAA"), cleaner.cleanInclusion("AAA,AA"));
            CPPUNIT_ASSERT_EQUAL(string("AAA"), cleaner.cleanInclusion("AA,AAA"));
            CPPUNIT_ASSERT_EQUAL(string("AAA,B"), cleaner.cleanInclusion("AA,AAA,B"));
            CPPUNIT_ASSERT_EQUAL(string("AAA"), cleaner.cleanInclusion("AA,AAA,AA"));
            CPPUNIT_ASSERT_EQUAL(string("AAA"), cleaner.cleanInclusion("AA,AAA,AA,A"));
            CPPUNIT_ASSERT_EQUAL(string("AAAA"), cleaner.cleanInclusion("AA,AAAA,AA,A"));
            CPPUNIT_ASSERT_EQUAL(string("AAA"), cleaner.cleanInclusion("AAA,A"));
            CPPUNIT_ASSERT_EQUAL(string("B,AAA"), cleaner.cleanInclusion("B,AAA,A"));
            CPPUNIT_ASSERT_EQUAL(string("AAA,B"), cleaner.cleanInclusion("AAA,B"));
            CPPUNIT_ASSERT_EQUAL(string("AAV"), cleaner.cleanInclusion("AAV,AA"));
            CPPUNIT_ASSERT_EQUAL(string("ATAT,QLQ,DSM"), cleaner.cleanInclusion("AT,ATA,ATAT,QL,QLQ,DSM"));
        }

        void testCleanLineInclusion2()
        {
            TxmbaCleaner cleaner = TxmbaCleaner("a", CleanMode::superstring,"b");
            CPPUNIT_ASSERT_EQUAL(string("QQGH,TPLH"), cleaner.cleanInclusion("QQGH,TPLH"));
            CPPUNIT_ASSERT_EQUAL(string("TTTTT"), cleaner.cleanInclusion("TTTTT,TTTT"));
            CPPUNIT_ASSERT_EQUAL(string("GFTPLHIA"), cleaner.cleanInclusion("GFTPLHIA,GFTPL"));
            CPPUNIT_ASSERT_EQUAL(string("QQQQQQQQQQQ"), cleaner.cleanInclusion("QQQQ,QQQQQQQQQQQ,QQQQQQQQ"));
            CPPUNIT_ASSERT_EQUAL(string("QQQQQQQQQQ,AACA,CKA"), cleaner.cleanInclusion("QQQQQ,QQQQQQQQQQ,QQQQ,AACA,CKA"));
            CPPUNIT_ASSERT_EQUAL(string("GFTPLHIA,QQGH"), cleaner.cleanInclusion("GFTPLHIA,QQGH,LHIA"));
            CPPUNIT_ASSERT_EQUAL(string("AAAAAAAA"), cleaner.cleanInclusion("AAAAAAAA,AAAA"));
            CPPUNIT_ASSERT_EQUAL(string("QQGH,GFTPLHIA"), cleaner.cleanInclusion("QQGH,GFTPLHIA"));
            CPPUNIT_ASSERT_EQUAL(string(""), cleaner.cleanInclusion(""));
            CPPUNIT_ASSERT_EQUAL(string("AACTGNLE,AASNEK,ACNSS,AFLEEL,AKSFN,ALKLNR,CEEEP,CERRY,CNSSN,CSQQM,CYYSL,DAVKY"), cleaner.cleanInclusion("AACT,AACTG,AACTGN,AACTGNL,AACTGNLE,AASN,AASNE,AASNEK,ACNS,ACNSS,ACTG,AFLE,AFLEE,AFLEEL,AKSF,AKSFN,ALKL,ALKLN,ALKLNR,CEEE,CEEEP,CERR,CERRY,CNSS,CNSSN,CSQQ,CSQQM,CTGN,CTGNL,CYYS,CYYSL,DAVK,DAVKY"));
        }

        void testCleanLineExclusion1()
        {
            TxmbaCleaner cleaner = TxmbaCleaner("a", CleanMode::substring,"b");
            CPPUNIT_ASSERT_EQUAL(string("QQGH,TPLH"), cleaner.cleanExclusion("QQGH,TPLH"));
            CPPUNIT_ASSERT_EQUAL(string("TTTT"), cleaner.cleanExclusion("TTTTT,TTTT"));
            CPPUNIT_ASSERT_EQUAL(string("GFTPL"), cleaner.cleanExclusion("GFTPLHIA,GFTPL"));
            CPPUNIT_ASSERT_EQUAL(string("QQQQ"), cleaner.cleanExclusion("QQQQ,QQQQQQQQQQQ,QQQQQQQQ"));
            CPPUNIT_ASSERT_EQUAL(string("QQQQ,AACA,CKA"), cleaner.cleanExclusion("QQQQQ,QQQQQQQQQQ,QQQQ,AACA,CKA"));
            CPPUNIT_ASSERT_EQUAL(string("QQGH,LHIA"), cleaner.cleanExclusion("GFTPLHIA,QQGH,LHIA"));
            CPPUNIT_ASSERT_EQUAL(string("AAAA"), cleaner.cleanExclusion("AAAAAAAA,AAAA"));
            CPPUNIT_ASSERT_EQUAL(string("QQGH,GFTPLHIA"), cleaner.cleanExclusion("QQGH,GFTPLHIA"));
            CPPUNIT_ASSERT_EQUAL(string("AT"), cleaner.cleanExclusion("AT,ATAT,ATA,ATB"));
            CPPUNIT_ASSERT_EQUAL(string("AACT,AASN,ACNS,ACTG,AFLE,AKSF,ALKL,CEEE,CERR,CNSS,CSQQ,CTGN,CYYS,DAVK"), cleaner.cleanExclusion("AACT,AACTG,AACTGN,AACTGNL,AACTGNLE,AASN,AASNE,AASNEK,ACNS,ACNSS,ACTG,AFLE,AFLEE,AFLEEL,AKSF,AKSFN,ALKL,ALKLN,ALKLNR,CEEE,CEEEP,CERR,CERRY,CNSS,CNSSN,CSQQ,CSQQM,CTGN,CTGNL,CYYS,CYYSL,DAVK,DAVKY"));
        }

        void testFileCleanerExclusion()
        {
            TxmbaCleaner cleaner = TxmbaCleaner("tests/cleaner/tx1.txt", CleanMode::substring, "tests/cleaner/tx1.inclusion.result.txt");
            cleaner.cleanLines();
            CPPUNIT_ASSERT_EQUAL(string(""), runCommand("diff tests/cleaner/tx1.exclusion.expected.txt tests/cleaner/tx1.exclusion.result.txt"));
            runCommand("./cleaner tests/cleaner/tx1.txt 0 tests/cleaner/tx1.exclusion.result2.txt");
            CPPUNIT_ASSERT_EQUAL(string(""), runCommand("diff tests/cleaner/tx1.exclusion.expected.txt tests/cleaner/tx1.exclusion.result2.txt"));
        }        

        void testFileCleanerInclusion()
        {
            TxmbaCleaner cleaner = TxmbaCleaner("tests/cleaner/tx1.txt", CleanMode::superstring, "tests/cleaner/tx1.inclusion.result.txt");
            cleaner.cleanLines();
            CPPUNIT_ASSERT_EQUAL(string(""), runCommand("diff tests/cleaner/tx1.inclusion.expected.txt tests/cleaner/tx1.inclusion.result.txt"));
            runCommand("./cleaner tests/cleaner/tx1.txt 1 tests/cleaner/tx1.inclusion.result2.txt");
            CPPUNIT_ASSERT_EQUAL(string(""), runCommand("diff tests/cleaner/tx1.inclusion.expected.txt tests/cleaner/tx1.inclusion.result2.txt"));
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

        string runCommand(string command)
        {
            //cout << "Running command...  '" << command << "'" << endl;
            char buffer[512];
            string result = "";
            FILE* pipe = popen(command.c_str(), "r");
            if (!pipe) throw std::runtime_error("popen() failed!");
            try {
                while (!feof(pipe)) {
                    if (fgets(buffer, 512, pipe) != NULL)
                        result += buffer;
              }
            } catch (...) {
              pclose(pipe);
              throw;
            }
            pclose(pipe);
            boost::algorithm::trim(result);
            return result;
        }

};

CPPUNIT_TEST_SUITE_REGISTRATION( TxmbaCleanerTest );

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