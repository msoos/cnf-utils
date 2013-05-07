#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import os
import fnmatch
import gzip
import re
import getopt, sys
import sys

def check_regular_clause(line, maxvar):
    lits = line.split()
    for lit in lits :
        numlit = int(lit)
        var = abs(numlit)

        #end of line
        if (var == 0) :
            break

        #regular variable
        maxvar = max(var, maxvar)
    return maxvar

def doit(fname):
    print "c Examining CNF file %s" %(fname)

    if fname[-3:] == ".gz" :
        f = gzip.open(fname, "r")
    else :
        f = open(fname, "r")

    maxvar = 0
    clauses = 0
    for line in f :
        #print "Examining line '%s'" %(line)
        line = line.rstrip()
        if (len(line) == 0) :
            continue

        if (line[0] != 'c' and line[0] != 'p') :
            if (line[0] != 'x') :
                maxvar = check_regular_clause(line, maxvar)
            else :
                print "OOOOPS! -- xor-clause"
                exit(-1);
                #self.check_xor_clause(line)
            clauses += 1

    f.close()

    #open input file
    if fname[-3:] == ".gz" :
        f = gzip.open(fname, "r")
    else :
        f = open(fname, "r")

    #write to output
    print "p cnf %d %d" % (maxvar, clauses)
    for line in f :
        #skip header
        line = line.rstrip().lstrip()
        if len(line) == 0 or line[0] == "p" or line[0] == "c" :
            continue

        print line

    #finish up
    f.close()

doit(sys.argv[1])

