#!/usr/bin/env python3

"""
    CNF reduce
    ~~~~~~~~~~

    Given a CNF file and a partial assignment.
    Reduce the CNF file content with the assignment given.

    Two files are required. One file containing a CNF in DIMACS format::

        p cnf 6 4
        1 2 3 4 0
        5 4 2 1 0
        2 3 6 0
        -2 0

    Secondly, an assignment file is given::

        -2

    Invoking this script with both files and an output path as parameters,
    it will write a file containing::

        p cnf 6 3
        1 3 4 0
        5 4 1 0
        3 6 0

    Note. The number of variable will not be changed!

    (C) 2015, Public Domain, Lukas Prokop
"""

import re
import argparse


# Note. You can also supply the partial assignment here
assignment = {
    #1: False, 2: False, 3: True, 4: True, 5: False, ...
}


def read_integers(fd):
    """Read a white-space separated integers from a file
    and return them in a generator.

    :param fd:      a file descriptor
    :type fd:       _io.TextIOWrapper
    :return:        a generator for integers
    :rtype:         <generator int>
    """
    for line in fd:
        for match in re.finditer('-?(\d+)', line):
            yield int(match.group(0))


def read_dimacs(fd):
    """Given a file descriptor for a DIMACS file,
    read nbvars, nbclauses and the list of clauses.
    Return those three values.

    :param fd:      a file descriptor
    :type fd:       _io.TextIOWrapper
    :return:        (nbvars, nbclauses, list of clauses)
    :rtype:         (int, int, [{int,}])
    """
    clauses, clause = [], []
    nbvars, nbclauses = 0, 0

    for i, lit in enumerate(read_integers(fd)):
        if i == 0:
            nbvars = lit
            continue
        elif i == 1:
            nbclauses = lit
            continue
        if lit == 0:
            if clause:
                clauses.append(tuple(clause))
            clause = []
        else:
            clause.append(lit)
    if clause:
        clauses.append(tuple(clause))
    return nbvars, nbclauses, clauses


def reduce_clauses(clauses, assignment):
    """Given a list of clauses and a set of assignment values.
    Return the reduced clauses.

    :param clauses:         a list of integer tuples
    :type clauses:          [(int,)]
    :param assignment:      a set of assignments (non-zero signed or unsigned integers)
    :type assignment:       {int,}
    :return:                a list of integer tuples
    :rtype:                 [(int,)]
    """
    new_clauses = []
    for clause in clauses:
        new_clause = []
        for lit in clause:
            if lit in assignment:
                new_clause = []
                break
            elif -lit in assignment:
                continue
            else:
                new_clause.append(lit)
        if new_clause:
            new_clauses.append(new_clause)
    return new_clauses


def write_dimacs(fd, clauses, nbvars, nbclauses):
    """Given a writable file descriptor. Write clauses in DIMACS format to it.

    :param fd:          a file descriptor
    :type fd:           _io.TextIOWrapper
    :param clauses:     clauses to write
    :type clauses:      list of clauses
    :param nbvars:      number of variables used clauses
    :type nbvars:       int
    :param nbclauses:   the number of clauses to be written
    """
    fd.write('p cnf {} {}\n'.format(nbvars, nbclauses))
    for clause in clauses:
        for lit in clause:
            fd.write('{} '.format(lit))
        fd.write('0\n')


def main():
    """Main routine"""
    global assignment

    desc = 'Reduce a CNF with a given partial assignment.'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('cnffile', type=argparse.FileType('r', encoding='ascii'),
                        help='DIMACS file providing a CNF')
    if not assignment:
        parser.add_argument('assignmentfile',
                            type=argparse.FileType('r', encoding='ascii'),
                            help='file containing partial assignment')
    parser.add_argument('outfile', type=argparse.FileType('x', encoding='ascii'),
                        help='output DIMACS file to write')
    args = parser.parse_args()

    if not assignment:
        assignment = set(read_integers(args.assignmentfile))

    if not assignment:
        raise ValueError('partial assignment empty - nothing to do')

    nbvars, nbclauses, clauses = read_dimacs(args.cnffile)
    new_clauses = reduce_clauses(clauses, assignment)
    write_dimacs(args.outfile, new_clauses, nbvars, len(new_clauses))

    print('Reduced {} to {} clauses'.format(nbclauses, len(new_clauses)))
    print('File {} written.'.format(args.outfile.name or 'has been'))


if __name__ == '__main__':
    main()
