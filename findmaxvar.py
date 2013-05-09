#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
f = open(sys.argv[1], "r")
maxvar = 0
for line in f :
    if len(line) == 0:
        continue

    for v in line.split() :
        v = v.lstrip().rstrip()
        if v == "d" :
            continue

        maxvar = max(maxvar, abs(int(v)))

print "maxvar: ", maxvar