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

parser = optparse.OptionParser(usage=usage, description=desc, formatter=PlainHelpFormatter())

#parser.add_option("--infile", dest="input_file", required=True, metavar="INFILE"
                    #, default=None
                    #, help="Convert this file with XORs"
                    #)
#parser.add_option("--outfile", dest="output_file", required=True, metavar="OUTFILE"
                    #, default=None
                    #, help="Against this solution"
                    #)

(options, args) = parser.parse_args()

if len(args) != 2 :
    print "ERROR: You must give 2 files as positional arguments, these will be the input and the output, respectively"
    exit(-1)

xortocnf = XorToCNF()
xortocnf.convert(args[0], args[1])

