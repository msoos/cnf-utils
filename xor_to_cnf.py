#!/usr/bin/env python

import optparse
from xor_to_cnf_class import *

usage = "usage: %prog [options] INFILE OUTFILE"
desc = """Converts a CNF that contains XOR clauses to regular CNF
"""

class PlainHelpFormatter(optparse.IndentedHelpFormatter):
    def format_description(self, description):
        if description:
            return description + "\n"
        else:
            return ""

xortocnf = XorToCNF()
parser = optparse.OptionParser(usage=usage, description=desc, formatter=PlainHelpFormatter())

parser.add_option("--cutsize", dest="cutsize", metavar="CUTSIZE", type=int
                    , default=xortocnf.cutsize
                    , help="The size of the XOR where it's 'cut'. If it's 4, the XORs will first be cut into 4-long chunks (with extra variables included) and then converted to regular clauses each of size 8(=2**(cutsize-1))"
                    )

(options, args) = parser.parse_args()

if len(args) != 2 :
    print "ERROR: You must give 2 files as positional arguments, these will be the input and the output, respectively"
    exit(-1)


xortocnf.cutsize = options.cutsize
xortocnf.convert(args[0], args[1])

