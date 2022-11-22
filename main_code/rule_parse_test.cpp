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
#include "rule_parse_and_match.h"

class RuleParseTest : public CppUnit::TestFixture
{

    private:
        CPPUNIT_TEST_SUITE( RuleParseTest );
        CPPUNIT_TEST( testParseRuleIntoItemlist );
        CPPUNIT_TEST( testLoadProteinListFromFolder );
        CPPUNIT_TEST( testWriteRules );
        CPPUNIT_TEST( testGetConsequentOfRule );
        CPPUNIT_TEST( testGetAlignedSequences );

        CPPUNIT_TEST_SUITE_END();

    public:
        void setUp() {}

        void tearDown() {}

        void testParseRuleIntoItemlist()
        {
            RuleParser rp = RuleParser("ruleFileFake", "tests/freq-dist/2", "tests/ruleparser/1/out/");
            itemlist expected1 = {"A","B","C"};
            itemlist expected2 = {"GKTAL","GKTA"};

            itemlist items1 = rp.parseRule("{A,B} => {C}");
            itemlist items2 = rp.parseRule("{GKTAL} => {GKTA}");

            assertEqualVectors(expected1, items1);
            assertEqualVectors(expected2, items2);
        }

        void testLoadProteinListFromFolder()
        {
            RuleParser rp = RuleParser("ruleFileFake", "tests/freq-dist/2","tests/ruleparser/1/out/");
            string encoding1 = "SDLGKKLLEAARAGQDDEVRILMANGADVNAEDKVGLTPL"
"HLAAMNDHLEIVEVLLKNGADVNAIDAIGETPLHLVAMYG"
"HLEIVEVLLKHGADVNAQDKFGKTAFDISIDNGNEDLAEI"
"LQKL";
            Protein p1 = Protein(encoding1, "tests/freq-dist/2/p1.fasta");

            string encoding2 = "SDLGKKLLEAARAGQDDEVRILMANGADVNANDWFGITPL"
"HLVVNNGHLEIIEVLLKYAADVNASDKSGWTPLHLAAYRG"
"HLEIVEVLLKYGADVNAMDYQGYTPLHLAAEDGHLEIVEV"
"LLKYGADVNAQDKFGKTAFDISIDNGNEDLAEILQ";
            Protein p2 = Protein(encoding2, "tests/freq-dist/2/p2.fasta");

            vector<Protein> expectedList = {p2, p1};
            vector<Protein> actualList = rp.loadProteins();

            //assertEqualVectors(expectedList, rp.loadProteins());
            CPPUNIT_ASSERT_EQUAL(expectedList.size(), actualList.size());
            for(unsigned int i = 0; i < actualList.size(); i++) {
                CPPUNIT_ASSERT_EQUAL(expectedList[i].getEncoding(), actualList[i].getEncoding());
            }
        }

        /**
         * [testWriteRules description]
         * @skipped
         */
        void testWriteRules()
        {
            RuleParser rp = RuleParser("tests/ruleparser/1/in/rules.txt", "tests/ruleparser/1/in/proteins","tests/ruleparser/1/out/");
            rp.processRuleFile();
        }

        /**
         * Get the consequent of the rule (ie. the last item from the parsed rule)
         */
        void testGetConsequentOfRule()
        {
            RuleParser rp = RuleParser("ruleFileFake", "tests/freq-dist/2", "tests/ruleparser/1/out/");

            itemlist items1 = rp.parseRule("{A,B} => {C}");
            itemlist items2 = rp.parseRule("{GKTAL} => {GKTA}");
            itemlist items3 = rp.parseRule("{KK,II,LL,MM} => {RRR}");

            CPPUNIT_ASSERT_EQUAL(string("C"), rp.extractConsequentFromParsedRule(items1));
            CPPUNIT_ASSERT_EQUAL(string("GKTA"), rp.extractConsequentFromParsedRule(items2));
            CPPUNIT_ASSERT_EQUAL(string("RRR"), rp.extractConsequentFromParsedRule(items3));
            CPPUNIT_ASSERT_EQUAL(string("p1.fasta"), string(basename("tests/holi/p1.fasta")));
        }

        void testGetAlignedSequences()
        {
            string protein = "AAAA01CB23AAAAA";
            string fragment = "CB";

            RuleParser rp = RuleParser("ruleFileFake", "tests/freq-dist/2", "tests/ruleparser/1/out/");

            CPPUNIT_ASSERT_EQUAL(string("01CB23"), rp.getAlignedSequences(protein, fragment)[0]);

            string protein2 = "AAAA01CB23AAACB";
            
            auto matches = rp.getAlignedSequences(protein2, fragment);
            CPPUNIT_ASSERT_EQUAL(string("01CB23"), matches[0]);                
            CPPUNIT_ASSERT_EQUAL(string("AACBXX"), matches[1]);                
            
            matches = rp.getAlignedSequences(fragment, fragment);
            CPPUNIT_ASSERT_EQUAL(string("XXCBXX"), matches[0]);                

            string protein3 = "CB009910101";
            matches = rp.getAlignedSequences(protein3, fragment);
            CPPUNIT_ASSERT_EQUAL(string("XXCB00"), matches[0]);

            matches = rp.getAlignedSequences(protein3, string("10"));
            CPPUNIT_ASSERT_EQUAL(string("991010"), matches[0]);
            CPPUNIT_ASSERT_EQUAL(string("10101X"), matches[1]);

            matches = rp.getAlignedSequences(protein3, string("1"));
            CPPUNIT_ASSERT_EQUAL(string("99101"), matches[0]);
            CPPUNIT_ASSERT_EQUAL(string("10101"), matches[1]);
            CPPUNIT_ASSERT_EQUAL(string("101XX"), matches[2]);

            matches = rp.getAlignedSequences(protein3, string("00"));
            CPPUNIT_ASSERT_EQUAL(string("CB0099"), matches[0]);
        }

        template<typename T>
        void assertEqualVectors(const vector<T>& v1, const vector<T>& v2)
        {
            CPPUNIT_ASSERT_EQUAL(v2.size(), v2.size());
            for(unsigned int i = 0; i < v1.size(); i++) {
                CPPUNIT_ASSERT_EQUAL(v1[i], v2[i]);
            }
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

};

CPPUNIT_TEST_SUITE_REGISTRATION( RuleParseTest );

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