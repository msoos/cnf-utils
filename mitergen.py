#!/usr/bin/env python3
# Miter of a random AND/XOR circuit and structurally equivalent copies: UNSAT,
# or likely SAT with --mutate. Exercises congruence closure. Usage: mitergen.py [--mutate] SEED
import random
import sys

args = [a for a in sys.argv[1:] if a != "--mutate"]
mutate = "--mutate" in sys.argv[1:]
random.seed(int(args[-1]) if args else 0)

nvars = 0
cls = []

def new_var():
    global nvars
    nvars += 1
    return nvars

def and_gate(ins):
    o = new_var()
    for x in ins:
        cls.append([-o, x])
    cls.append([o] + [-x for x in ins])
    return o

def xor_gate(ins):
    o = new_var()
    vs = [o] + ins
    n = len(vs)
    for bits in range(1 << n):
        # clause forbids the assignment whose parity makes o != XOR(ins)
        assign = [(bits >> k) & 1 for k in range(n)]
        if sum(assign) % 2 == 1:
            cls.append([-v if assign[k] else v for k, v in enumerate(vs)])
    return o

n_in = random.randint(3, 20)
n_gates = random.randint(5, 120)
spec = []
for g in range(n_gates):
    typ = random.choice(["and", "and", "xor"])
    arity = random.randint(2, 3) if typ == "xor" else random.randint(2, 4)
    if random.random() < 0.9:
        picks = random.sample(range(n_in + g), min(arity, n_in + g))
    else:
        picks = [random.randrange(n_in + g) for _ in range(arity)]
    srcs = [(x, random.random() < 0.5) for x in picks]
    spec.append((typ, srcs))
outs = random.sample(range(n_in + n_gates), min(random.randint(1, 4), n_in + n_gates))

inputs = [new_var() for _ in range(n_in)]

def build(mut):
    nodes = list(inputs)
    for idx, (typ, srcs) in enumerate(spec):
        srcs = list(srcs)
        random.shuffle(srcs)
        if mut and idx == mut:
            typ = "xor" if typ == "and" else "and"
        if typ == "xor":
            # XOR(a,b) == XOR(-a,-b): flip pairs of negations
            if len(srcs) >= 2 and random.random() < 0.5:
                srcs[0] = (srcs[0][0], not srcs[0][1])
                srcs[1] = (srcs[1][0], not srcs[1][1])
            ins = [-nodes[s] if neg else nodes[s] for s, neg in srcs]
            nodes.append(xor_gate(ins))
        else:
            ins = [-nodes[s] if neg else nodes[s] for s, neg in srcs]
            nodes.append(and_gate(ins))
    return nodes

copies = [build(0) for _ in range(random.randint(2, 3))]
if mutate:
    copies.append(build(random.randrange(1, n_gates) if n_gates > 1 else 0))

diffs = []
for c in copies[1:]:
    for o in outs:
        diffs.append(xor_gate([copies[0][o], c[o]]))
cls.append(diffs)

perm = list(range(1, nvars + 1))
random.shuffle(perm)
ren = lambda l: perm[abs(l) - 1] * (1 if l > 0 else -1)
random.shuffle(cls)
print("p cnf %d %d" % (nvars, len(cls)))
for c in cls:
    print(" ".join(str(ren(l)) for l in c) + " 0")
