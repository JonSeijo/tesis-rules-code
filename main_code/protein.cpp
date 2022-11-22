#include "protein.h"

/*
bool Protein::operator==(const Protein& l) const
{
    return this->getEncoding() == l.getEncoding();
}

bool Protein::operator!=(const Protein& l) const
{
    return this->getEncoding() != l.getEncoding();
}
*/

Protein::Protein(string enc, string fname)
{
    encoding = enc;
    filename = fname;
}

const string Protein::getEncoding() const
{
    return encoding;
}

const string Protein::getFilename() const
{
    return filename;
}

map<char,int> Protein::getAminoSummary()
{
    map<char,int> summary;
    for (std::string::iterator it = encoding.begin(); it != encoding.end(); ++it) {
       if (summary.count(*it)>0) {
            summary[*it]++;
       } else {
            summary[*it] = 1;
       }
    }

    return summary;
}

int Protein::getLength()
{
    return encoding.length();
}

void Protein::combineSummary(const map<char,int>& freqInfo, map<char,int>& acumulator)
{
    for(auto& entry: freqInfo) {
        std::map<char,int>::iterator it;
        it = acumulator.find(entry.first);
        if (it != acumulator.end()) {
            acumulator[entry.first] += entry.second;
        } else {
            acumulator[entry.first] = entry.second;
        }

    }
}

/*
ostream& operator<<(ostream& out, const Protein& l) {
    out << l.getEncoding();
    return out;
}
*/