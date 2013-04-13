#include "solvertypes.h"
#include "MersenneTwister.h"
#include <vector>
#include <iostream>
#include <time.h>

using std::endl;
using std::cout;
using std::vector;
using CMSat::Lit;

/*struct Clause
{
    vector<Lit> lits;
};

std::ostream& operator<<(std::ostream& os, const Clause& cl)
{
    for(size_t i = 0; i < cl.lits.size(); i++) {
        os << cl[i];
    }

    os << "0" << endl;

    return os;
}*/

static MTRand mtrand;
static uint64_t numVars;

int main()
{
    mtrand.seed(time(NULL));
    numVars = mtrand.randInt(10ULL*1000ULL*1000ULL) + 5ULL*1000ULL*1000ULL;

    //Create MANY larege clauses
    for(size_t i = 0, end = mtrand.randInt(150000)
        ; i < end
        ; i++
    ) {
        size_t size = mtrand.randInt(250);
        size += 200;
        for(size_t i2 = 0; i2 < size; i2++) {
            cout
            << Lit(mtrand.randInt(numVars), mtrand.randInt(1))
            << " ";
        }
        cout << "0" << endl;
    }

    vector<char> alreadyHit;
    alreadyHit.resize((numVars+1)*2, 0);

    //Lots of long binary chains
    Lit lit = Lit(mtrand.randInt(numVars), mtrand.randInt(1));
    for(size_t i = 0, end = mtrand.randInt(40)
        ; i < end
        ; i++
    ) {
        //Pick a fresh one that hasn't been hit yet
        do {
            lit = Lit(
                mtrand.randInt(numVars)
                , mtrand.randInt(1)
            );
        } while(alreadyHit[lit.toInt()] == 1);
        assert(alreadyHit[lit.toInt()] == 0);
        alreadyHit[lit.toInt()] = 1;

        //And chain to it
        size_t size = mtrand.rand(i*10);
        for(size_t i2 = 0; i2 < size; i2++) {

            //Chain linearly
            Lit lit2;
            for(size_t i3 = 0, i3size = mtrand.randInt(500) + 40
                ; i3 < i3size
                ; i3++
            ) {
                do {
                    lit2 = Lit(
                        mtrand.randInt(numVars)
                        , mtrand.randInt(1)
                    );
                } while(alreadyHit[lit2.toInt()] == 1);
                assert(alreadyHit[lit2.toInt()] == 0);
                alreadyHit[lit2.toInt()] = 1;

                //print binary
                cout
                << ~lit
                << " "
                << lit2
                << " 0" << endl;
            }

            //Chain next one
            lit = lit2;
        }
    }
}