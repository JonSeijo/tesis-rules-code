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
#include "scrambler.h"

#define MODE_SCRAMBLE 1
#define MODE_UNIFORM 2

class ScramblerTest : public CppUnit::TestFixture
{

    private:
        CPPUNIT_TEST_SUITE( ScramblerTest );
        CPPUNIT_TEST( testScrambleCreatedOk );
        CPPUNIT_TEST( testScrambleProtein );
        CPPUNIT_TEST( testCodeIsInBounds );
        CPPUNIT_TEST( testApproximateUniformDistribution );
        CPPUNIT_TEST( testGenerateUniformStrings );
        CPPUNIT_TEST( testGenerateVariationsFromInputDir );
        CPPUNIT_TEST( testReplacePathOk );
        
        CPPUNIT_TEST_SUITE_END();

    public:
        void setUp() {}

        void tearDown() {}

        void testScrambleCreatedOk()
        {
            Scrambler s = Scrambler("tests/scrambler/in", "output");
            CPPUNIT_ASSERT_EQUAL(string("output"), s.outputDirectory);
        }

        void testScrambleProtein()
        {
            Scrambler s = Scrambler("tests/scrambler/in", "output");
            string input = "ASFSDFASDFSFS";
            string scrambled = s.scramble(input);
            CPPUNIT_ASSERT(scrambled != input);
            CPPUNIT_ASSERT_EQUAL(scrambled.size(), input.size());
            CPPUNIT_ASSERT_EQUAL(input, string("ASFSDFASDFSFS"));
        }

        void testUniformIsNotEqualToInput()
        {
            Scrambler s = Scrambler("tests/scrambler/in", "output");
            string input = "ASFSDFASDFSFS";
            string scrambled = s.uniform(13);
            CPPUNIT_ASSERT(scrambled != input);
            CPPUNIT_ASSERT_EQUAL(scrambled.size(), input.size());
        }

        void testCodeIsInBounds()
        {
            Scrambler s = Scrambler("tests/scrambler/in", "output");
            for(int i = 0; i < 100; i++) {
                int code = s.getRandomAminoAcidCode();
                CPPUNIT_ASSERT(code <= 19);
                CPPUNIT_ASSERT(code >= 0);
            }
        }

        void testApproximateUniformDistribution()
        {
            Scrambler s = Scrambler("tests/scrambler/in", "output");
            unsigned long int acum = 0;
            for(int i = 0; i < 10000; i++) {
                acum += s.getRandomAminoAcidCode();
            }

            float sampleMean = acum/10000.0;
            CPPUNIT_ASSERT_DOUBLES_EQUAL(9.5, sampleMean, 0.3);
        }

        void testGenerateUniformStrings()
        {
            Scrambler s = Scrambler("tests/scrambler/in", "output");
            unsigned long int sizes[] = {5,10,20,50,100,300};

            for(int i = 0; i < 6; i++) {
                string uniform = s.uniform(sizes[i]);
                //cout << endl << uniform << endl;
                CPPUNIT_ASSERT_EQUAL(sizes[i], uniform.length());
            }
        }

        void testGenerateVariationsFromInputDir()
        {
            Scrambler s = Scrambler("tests/scrambler/in", "tests/scrambler/out-uniform");
            s.generateVariations(MODE_UNIFORM);
        }

        void testReplacePathOk()
        {
            string input = "tests/scrambler/in/p1.fasta";
            string output = "tests/scrambler/out-uniform";
            string expected = "tests/scrambler/out-uniform/p1-uniform.fasta";

            string processed = input;
            replace(processed, string("tests/scrambler/in"), output);
            replace(processed, string(".fasta"), string("-uniform.fasta"));
            CPPUNIT_ASSERT_EQUAL(expected, processed);
        }

        bool replace(string& str, const string& from, const string& to)
        {
            size_t start_pos = str.find(from);
            if(start_pos == std::string::npos)
                return false;
            str.replace(start_pos, from.length(), to);
            return true;
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

CPPUNIT_TEST_SUITE_REGISTRATION( ScramblerTest );

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