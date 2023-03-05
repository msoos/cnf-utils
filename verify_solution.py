#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2009-2020 Authors of CryptoMiniSat, see AUTHORS file
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA

from __future__ import with_statement  # Required in 2.5
from __future__ import print_function
import gzip
import re
import fnmatch
import sys

def parse_solution_from_output(output_lines):
    if len(output_lines) == 0:
        print("Error! SAT solver output is empty!")
        print("output lines: %s" % output_lines)
        exit(-1)

    # solution will be put here
    satunsatfound = False
    vlinefound = False
    solution = {}
    sat = None

    # parse in solution
    for line in output_lines:
        # skip comment
        if (re.match('^c', line)):
            continue

        # SAT/UNSAT
        if (re.match('^s ', line)):
            if (satunsatfound):
                print("ERROR: solution twice in solver output!")
                exit(-1)

            if 'UNSAT' in line:
                sat = False
                satunsatfound = True
                continue

            if 'SAT' in line:
                sat = True
                satunsatfound = True
                continue

            print("ERROR: line starts with 's' but no SAT/UNSAT on line")
            exit(-1)

        # parse in solution
        if (re.match('^v ', line)):
            vlinefound = True
            myvars = line.split(' ')
            for var in myvars:
                var = var.strip()
                if var == "" or var == 'v':
                    continue
                if (int(var) == 0):
                    break
                intvar = int(var)
                solution[abs(intvar)] = (intvar >= 0)
            continue

        if (line.strip() == ""):
            continue

        print("Error! SAT solver output contains a line that is neither 'v' nor 'c' nor 's'!")
        print("Line is:", line.strip())
        exit(-1)

    if (satunsatfound is False):
        print("Error: Cannot find if SAT or UNSAT. Maybe didn't finish running?")
        exit(-1)

    if (sat is True and vlinefound is False):
        print("Error: Solution is SAT, but no 'v' line")
        exit(-1)

    return sat, solution

def check_regular_clause(line, solution):
    lits = line.split()
    for lit in lits:
        numlit = int(lit)
        if numlit == 0:
            break

        if abs(numlit) not in solution:
            continue

        if solution[abs(numlit)] ^ (numlit < 0):
            return True

    # print not set vars
    for lit in lits:
        numlit = int(lit)
        if numlit == 0:
            break

        if abs(numlit) not in solution:
            print("var %d in XOR clause not set" % abs(numlit))

    print("Error: clause '%s' not satisfied." % line.strip())
    raise NameError("Error: clause '%s' not satisfied." % line)

def check_xor_clause(line, solution):
    line = line.lstrip('x')
    lits = line.split()
    final = False
    for lit in lits:
        numlit = int(lit)
        if numlit != 0:
            if abs(numlit) not in solution:
                raise NameError("Error: var %d not solved, but referred to in a xor-clause of the CNF" % abs(numlit))
            final ^= solution[abs(numlit)]
            final ^= numlit < 0
    if final is False:
        print("Error: xor-clause '%s' not satisfied." % line.strip())
        raise NameError("Error: xor-clause '%s' not satisfied." % line)

def test_found_solution(solution, fname):
    print("Verifying solution.")

    if fnmatch.fnmatch(fname, '*.gz'):
        f = gzip.open(fname, "r")
    else:
        f = open(fname, "r")
    clauses = 0

    for line in f:
        line = line.rstrip()

        # skip empty lines
        if len(line) == 0:
            continue

        # check solution against clause
        try:
            if line[0] != 'c' and line[0] != 'p':
                if line[0] != 'x':
                    check_regular_clause(line, solution)
                else:
                    assert line[0] == 'x', "Line must start with p, c, v or x"
                    check_xor_clause(line, solution)

            clauses += 1
        except:
            raise

    f.close()
    print("Verified %d original xor&regular clauses" % clauses)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR you must give CNF and SOLUTION files as arguments");
        exit(-1)

    cnf_fname = sys.argv[1];
    solution_fname = sys.argv[2];

    with open(solution_fname, "r") as sol_f:
        solution_txt = sol_f.read().split("\n")

    sat, solution = parse_solution_from_output(solution_txt)
    if not sat:
        print("It's UNSAT, we can't test this solution");
        exit(0);

    test_found_solution(solution, cnf_fname)
    print("Solution OK");

