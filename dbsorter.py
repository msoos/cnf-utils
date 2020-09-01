#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 Vegard Nossum
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys

#print "file: %s" % sys.argv[1]

def myabs(a) :
    return(abs(a))

f = open(sys.argv[1])
for line in f :
    if line[0] == "d" or line[0] == "p" or line[0] == "c":
        continue

    sp = [int(a) for a in line.split()]
    sp.sort(key=myabs)
    for i in sp :
        if i != 0 :
            sys.stdout.write("%s " % i)
    print "0"
