#!/usr/bin/env python3

import random
import sys
import optparse

parser = optparse.OptionParser()
parser.add_option("--seed", metavar="SEED", dest="seed", type=int,
                  help="seed value")
(options, args) = parser.parse_args()
if options.seed is not None:
    random.seed(options.seed)

numvars = random.randint(20, 200)
numunits = random.randint(0, 15)
numlongs = random.randint(numvars, numvars*3)
numcls = numunits + numlongs

xorclsizes = []
for i in range(random.randint(min(100, numvars), numvars)):
    thissize = random.randint(3, 7)
    xorclsizes.append(thissize)
    numcls += 1 << (thissize-1)

# own RNG: seeds keep their old clauses
long_rnd = random.Random("longcls%s" % options.seed) if options.seed is not None else random.Random()
numverylong = long_rnd.randint(1, 3) if long_rnd.randint(0, 9) == 0 else 0
numcls += numverylong

print("p cnf %d %d" % (numvars, numcls))

for i in range(numverylong):
    vs = long_rnd.sample(range(1, numvars+1), long_rnd.randint(min(numvars, 100), numvars))
    print(" ".join(str(v if long_rnd.randint(0, 1) else -v) for v in vs) + " 0")

#longcls
for i in range(numlongs):
    vars = set()
    for i2 in range(random.randint(2, 5)):
        lit = random.randint(1, numvars)
        if lit in vars: continue
        vars.add(lit)
        if random.randint(0, 1) == 1:
            lit = -1*lit
        sys.stdout.write("%d " % lit)

    print("0")

#units
for i in range(numunits):
    lit = random.randint(1, numvars)
    if random.randint(0, 1) == 1:
        lit = -1*lit
    print("%d 0" % lit)

#xors
for thisxorsize in xorclsizes:
    varlist = []

    #create varlist
    for a in range(thisxorsize):
        var = random.randint(1, numvars)
        while var in varlist:
            var = random.randint(1, numvars)

        #flip randomly
        if random.randint(0, 1) == 1:
            var = -1*var

        varlist.append(var)

    #polarity of the XOR
    polarity = random.randint(0, 1)

    for i2 in range(1 << len(varlist)):
        #number of inversions is right, use it
        if bin(i2).count("1") % 2 == polarity:
            at = 0
            for var in varlist:
                lit = var

                #calculate inversion
                invert = ((i2 >> at) & 1 == 1)
                #if polarity :
                #    invert = not invert

                #create lit
                if invert:
                    lit = -1*var

                #print lit
                sys.stdout.write("%d " % lit)
                at += 1

            #end of clause
            print("0")
