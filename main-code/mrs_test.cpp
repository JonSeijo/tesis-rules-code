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
#include <iostream>
#include <regex>

using namespace std;


class MrsTest : public CppUnit::TestFixture
{
    private:
        CPPUNIT_TEST_SUITE( MrsTest );
        CPPUNIT_TEST( testExecuteRunmrsAndOutputMatches );
        CPPUNIT_TEST( testParseOutputOfCommand );
        CPPUNIT_TEST( testPrepareCommand );
        CPPUNIT_TEST( testMfunction1 );
        CPPUNIT_TEST( testMfunction2 );
        CPPUNIT_TEST( testCoverage1 );
        CPPUNIT_TEST( testCoverage2 );
        CPPUNIT_TEST( testFamiliarity1 );
        CPPUNIT_TEST( testJoinProteinsToFile );


    CPPUNIT_TEST_SUITE_END();

    public:
        string s1 = "abcdeabcdfbcdebcd";
        string s4 = "abcdbcd";

        void setUp() {}
        void tearDown() {}

        // Parser tests
        void testExecuteRunmrsAndOutputMatches()
        {
            //Search and replace of tabs and newlines to avoid parsing problems.
            string result = "ABC (3)\n"
            "   3 0\n";
            Mrs mrs = Mrs::runMrs("ABCABC", '+', 2);
            CPPUNIT_ASSERT_EQUAL(result, mrs.getOutput());
        }

        void testPrepareCommand()
        {
            string result = "python ../turjanski/findpat/pyapi/runmrs.py \"ABCABB\" + 2";
            CPPUNIT_ASSERT_EQUAL(result, Mrs::prepareCommand("ABCABB", '+', 2));
        }

        void testParseOutputOfCommand()
        {
            string result = "ABC (3)\n"
            "   6 3 0 10\n"
            "ABCABC (6)\n"
            "   3 0";

            Mrs mrs = Mrs(result);
            map<string, vector<int> >* ocurrences = mrs.getOcurrences();
            map<string, int>* len = mrs.getLengths();

            CPPUNIT_ASSERT_EQUAL(3, (*len)["ABC"]);
            CPPUNIT_ASSERT_EQUAL(6, (*len)["ABCABC"]);
            CPPUNIT_ASSERT_EQUAL(3, (*ocurrences)["ABCABC"][0]);
            CPPUNIT_ASSERT_EQUAL(0, (*ocurrences)["ABCABC"][1]);
            CPPUNIT_ASSERT_EQUAL(6, (*ocurrences)["ABC"][0]);
            CPPUNIT_ASSERT_EQUAL(3, (*ocurrences)["ABC"][1]);
            CPPUNIT_ASSERT_EQUAL(0, (*ocurrences)["ABC"][2]);
            CPPUNIT_ASSERT_EQUAL(10, (*ocurrences)["ABC"][3]);
        }

        void testMfunction1()
        {
            Mrs mrs = Mrs::runMrs(this->s1, '+', 1);
            vector<string> sequences = mrs.m(3);

            CPPUNIT_ASSERT_EQUAL(std::string("abcd"), sequences[0]);
            CPPUNIT_ASSERT_EQUAL(std::string("bcde"), sequences[2]);
            CPPUNIT_ASSERT_EQUAL(std::string("bcd"), sequences[1]);
        }

        void testMfunction2()
        {
            Mrs mrs = Mrs::runMrs(this->s1, '+', 1);
            vector<string> sequences = mrs.m(4);

            CPPUNIT_ASSERT_EQUAL(std::string("abcd"), sequences[0]);
            CPPUNIT_ASSERT_EQUAL(std::string("bcde"), sequences[1]);
        }

        void testCoverage1()
        {
            std::vector<string> sequences = {"abcd", "bcde", "bcd"};
            float result = Famico::coverage(this->s1, sequences);
            float expectedCoverage = 16.0/17.0;
            CPPUNIT_ASSERT_EQUAL(expectedCoverage, result);
        }

        void testCoverage2()
        {
            std::vector<string> sequences = {"abcd", "bcde"};
            float result = Famico::coverage(this->s1, sequences);
            float expectedCoverage = 13.0/17.0;
            CPPUNIT_ASSERT_EQUAL(expectedCoverage, result);
        }

        void testFamiliarity1()
        {
            float result = Famico::familiarity(this->s4, this->s1);
            float expectedCoverage = 4.07143;
            CPPUNIT_ASSERT_DOUBLES_EQUAL(expectedCoverage, result, 0.00001);
        }

        string readFromFile(string filename)
        {
            std::ifstream infile(filename.c_str(), std::ifstream::in);
            std::string line;
            std::string contents;

            //Get length of file
            infile.seekg (0, infile.end);
            int length = infile.tellg();
            infile.seekg (0, infile.beg);

            if(length > 0) {
                while (std::getline(infile, line)) {
                    std::istringstream iss(line);
                    string currentLine = iss.str();

                    if(currentLine.length()>0) {
                        contents = contents + currentLine;
                    }
                }
            }

            return contents;
        }


        void testJoinProteinsToFile()
        {
            const char* path = "tests/join/";
            Mrs::joinProteinsToFile(path);
            string result = "SDLGKKLLEAARAGQDDEVRILMANGADVNANDWFGITPL"
"HLVVNNGHLEIIEVLLKYAADVNASDKSGWTPLHLAAYRG"
"HLEIVEVLLKYGADVNAMDYQGYTPLHLAAEDGHLEIVEV"
"LLKYGADVNAQDKFGKTAFDISIDNGNEDLAEILQ+"
"MADPEDPRDAGDVLGDDSFPLSSLANLFEVEDTPSPAEPSRGPPGAGDGKQNLRMKFHGA"
"FRKGPPKPMELLESTIYESSVVPAPKKAPMDSLFDYGTYRQHPSENKRWRRRVVEKPVAG"
"TKGPAPNPPPVLKVFNRPILFDIVSRGSPDGLEGLLSFLLTHKKRLTDEEFREPSTGKTC"
"LPKALLNLSAGRNDTIPILLDIAEKTGNMREFINSPFRDVYYRGQTALHIAIERRCKHYV"
"ELLVEKGADVHAQARGRFFQPKDEGGYFYFGELPLSLAACTNQPHIVHYLTENGHKQADL"
"RRQDSRGNTVLHALVAIADNTRENTKFVTKMYDLLLIKCAKLFPDTNLEALLNNDGLSPL"
"MMAAKTGKIGIFQHIIRREIADEDVRHLSRKFKDWAYGPVYSSLYDLSSLDTCGEEVSVL"
"EILVYNSKIENRHEMLAVEPINELLRDKWRKFGAVSFYISVVSYLCAMIIFTLIAYYRPM"
"EGPPPYPYTTTIDYLRLAGEIITLLTGILFFFSNIKDLFMKKCPGVNSFFIDGSFQLLYF"
"IYSVLVIVTAGLYLGGVEAYLAVMVFALVLGWMNALYFTRGLKLTGTYSIMIQKILFKDL"
"FRFLLVYLLFMIGYASALVSLLNPCPSSESCSEDHSNCTLPTYPSCRDSQTFSTFLLDLF"
"KLTIGMGDLEMLESAKYPGVFIILLVTYIILTFVLLLNMLIALMGETVGQVSKESKHIWK"
"LQWATTILDIERSFPLFLRRAFRSGEMVTVGKGTDGTPDRRWCFRVDEVNWSHWNQNLGI"
"ISEDPGKSDTYQYYGFSHTVGRLRRDRWSTVVPRVVELNKSCPTEDVVVPLGTMGTAEAR"
"ERRHGQTPSSPL";
        CPPUNIT_ASSERT_EQUAL(result, readFromFile("testsjoin-joined.txt"));
        }

};

CPPUNIT_TEST_SUITE_REGISTRATION( MrsTest );

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