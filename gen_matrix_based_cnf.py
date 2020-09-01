#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 Mate Soos
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
# 02110-1301, USA.

print("NOTE: this should import sage in some way")

def gen_cnf(n):
    A = random_matrix(GF(2),n,n+1)
    B = BooleanPolynomialRing(n,'x')
    v = Matrix(B, n+1, 1, B.gens() + (1,))
    l = (A*v).list()
    a2 = ANFSatSolver(B)
    s = a2.cnf(l)

    fname = "matrix%02d.cnf" % n
    print("written matrix CNF to file %s" % fname)
    open(fname).write(s)


gen_cnf(1)
