#!/usr/bin/env python3

# Copyright (C) 2019 Connor Olding
# Copyright (C) 2019 Mate Soos, minor modifications to randomize

# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# the original problem being solved was
# ((((x + ?) | ?) ... | ?) + ?) & 0x11111111 = expand4(x)
# where x is an n-bit variable (where n is the python `bit` variable)
# and the question marks are free 32-bit variables.

# this problem is trivial when AND gates are used
# in place of OR gates, but the form used here
# is more interesting to solve, in some sense.

# this problem has been randomized to fuzz the system

import random
import optparse

parser = optparse.OptionParser()
parser.add_option("--seed", metavar="SEED", dest="seed", type=int,
                  help="seed value")
(options, args) = parser.parse_args()
if options.seed is not None:
    random.seed(options.seed)

def expand4(x):
    return (
        (x & 1 << 0) << 0 |
        (x & 1 << 1) << 3 |
        (x & 1 << 2) << 6 |
        (x & 1 << 3) << 9 |
        (x & 1 << 4) << 12 |
        (x & 1 << 5) << 15 |
        (x & 1 << 6) << 18 |
        (x & 1 << 7) << 21)

class Problem:
    # NOTE: this class has been shrunk for the purposes of this test.

    def __init__(self):
        self.clauses = []
        self.i = 0
        self.names = {}

        self._counts = {}

        # shortcuts:
        self.ors = self.assign_or
        self.ands = self.assign_and
        self.xors = self.assign_xor
        self.nots = self.assign_not

    def var(self, name=None):
        self.i += 1
        if name is not None:
            self.names[self.i] = name
        return self.i

    def _new_temp(self, category, bits=None):
        count = self._counts.get(category, 0)
        varname = f'_{category}{count}_'
        if bits is None:
            bits = 1
            var_or_vars = self.var(varname)
        else:
            var_or_vars = [self.var(varname + str(i)) for i in range(bits)]
        self._counts[category] = count + bits
        return var_or_vars

    def add_clause(self, *args):
        for a in args:
            assert type(a) is int, type(a)
        self.clauses.append(args)

    def assert_or(self, *args):
        if len(args) == 0:
            return
        for a in args:
            if a is True:
                return
        args = [a for a in args if a is not False]
        if len(args) > 0:
            self.add_clause(*args)

    def assert_eq(self, a, b):
        self.assert_or(self.nots(self.xors(a, b)))

    def assign_or(self, *args):
        for a in args:
            if a is True:
                return True
        args = [a for a in args if a is not False]
        if len(args) == 0:
            return False
        elif len(args) == 1:
            return args[0]
        v = self._new_temp('or')
        for a in args:
            self.add_clause(v, -a)
        self.add_clause(-v, *args)
        return v

    def assign_and(self, *args):
        for a in args:
            if a is False:
                return False
        args = [a for a in args if a is not True]
        if len(args) == 0:
            return True
        elif len(args) == 1:
            return args[0]
        v = self._new_temp('and')
        for a in args:
            self.add_clause(-v, a)
        self.add_clause(v, *(-a for a in args))
        return v

    def assign_xor(self, a, *args):
        if len(args) == 0:
            return a
        b = args[0]
        if type(a) is bool:
            if type(b) is bool:
                v = (a or b) and (not a or not b)
            else:
                v = -b if a else b
        else:
            if type(b) is bool:
                v = -a if b else a
            else:
                v = self._new_temp('xor')
                self.add_clause(-v, -a, -b)
                self.add_clause(-v, a, b)
                self.add_clause(v, -a, b)
                self.add_clause(v, a, -b)
        for a in args[1:]:
            v = self.xors(v, a)
        return v

    def assign_not(self, a):
        if type(a) is bool:
            return not a
        else:
            return -a

    def adder(self, a, b, bits, return_carry=False):
        c = []
        carry = False
        for i in range(bits):
            t = self.xors(carry, self.xors(a[i], b[i]))
            c.append(t)
            if i + 1 != bits or return_carry:
                carry = self.xors(self.ands(a[i], b[i]),
                                  self.ands(carry, a[i]),
                                  self.ands(carry, b[i]))
        return (c, carry) if return_carry else c

    def dimacs(self, file=None, verbosity=1):
        print(f'p cnf {self.i} {len(self.clauses)}', file=file)
        if verbosity > 0:
            for ind, name in self.names.items():
                if name.startswith('_') and verbosity < 2:
                    continue
                print(f'c {ind} = {name}', file=file)
        for cls in self.clauses:
            print(*cls, 0, file=file)

bits = random.randint(3,7)
depth = bits * 2 - 3
depth += random.randint(0,10)
bigbits = random.randint(4,10)

p = Problem()

vars = [tuple([p.var(f'var{d}_{i}') for i in range(bigbits)])
        for d in range(depth)]

for b in range(1 << bits):
    x = b
    y = expand4(b)
    mask = random.randint(0, 2**32-1)

    inp = [bool(x & 1 << i) for i in range(bigbits)]

    for d in range(depth):
        if d % 2 == 0:
            out = p.adder(inp, vars[d], bigbits)
        else:
            out = [p.ors(i, o) for i, o in zip(inp, vars[d])]
        inp = out

    for i in range(bigbits):
        if mask & 1 << i:
            p.assert_eq(out[i], bool(y & 1 << i))

for _ in range(random.randint(0,80)):
    p.add_clause(
        random.choice([-1, 1])*random.randint(1, p.i),
        random.choice([-1, 1])*random.randint(1, p.i),
        random.choice([-1, 1])*random.randint(1, p.i),
        )

#p.dimacs(verbosity=2)
p.dimacs()
