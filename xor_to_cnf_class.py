import re

class XorToCNF :
    def __init__ (self):
        self.cutsize = 4

    def get_max_var(self, clause) :
        maxvar = 0

        clause = clause.strip()
        assert len(clause) > 0
        assert re.search(r'^x?-?\d+', clause)
        for lit in clause.split():
            var = abs(int(lit))
            maxvar = max(var, maxvar)

        return maxvar

    def convert(self, infilename, outfilename) :
        maxvar = self.get_max_var(infilename)

    def popcount(self, x):
        return bin(x).count('1')

    def parse_xor(self, xorclause):
        assert re.search(r'^x( *-?\d+ )*0$', xorclause)

        tmp = xorclause[1:]
        lits = [int(elem) for elem in tmp.split()]
        assert lits[len(lits)-1] == 0

        #remove last element, the 0
        lits = lits[:len(lits)-1]

        return lits


    def to_xor_simple(self, xorclause, equals = True) :
        assert equals == True or equals == False
        if equals == True:
            equals = 1
        else :
            equals = 0

        lits = self.parse_xor(xorclause)

        ret = []
        for i in range(2**(len(lits))) :
            #only the ones we need
            cls = ""
            if self.popcount(i) % 2 == equals:
                continue;

            for at in range(len(lits)) :
                if ((i>>at)&1) == 0:
                    cls += "%d " % lits[at]
                else:
                    cls += "%d " % (-1*lits[at])

            cls += "0"
            ret.append(cls)

        return ret

    def cut_up_xor_to_n(self, xorclause, oldmaxvar) :
        assert self.cutsize > 2
        lits = self.parse_xor(xorclause)
        assert lits > 4

        xors = []
        #print "numxorsret: ", num_xors_ret

        at = 0
        newmaxvar = oldmaxvar
        while(at < len(lits)):

            #until when should we cut?
            until = min(at + self.cutsize-1, len(lits))

            #if in the middle, don't add so much
            if at > 0 and until < len(lits) :
                until -= 1

            thisxor = "x"
            #print "from %d to %d" % (at, until)
            for i2 in range(at, until) :
                thisxor += "%d " % lits[i2]

            #add the extra variables
            if at == 0 :
                #beginning, add only one
                thisxor += "%d 0" % (newmaxvar+1)
                newmaxvar += 1
            elif until == len(lits) :
                #end, only add the one we already made
                thisxor += "%d 0" % (newmaxvar)
            else:
                thisxor += "%d %d 0" % (newmaxvar, newmaxvar+1)
                newmaxvar += 1

            xors.append(thisxor)

            #move along where we are at
            at = until

        return [xors, newmaxvar]

    def num_extra_vars_cls_needed(self, numlits) :
        varsneeded = 0
        clsneeded = 0

        at = 0
        while(at < numlits) :
            #at the beginning
            if at == 0 :
                if numlits > self.cutsize :
                    at += self.cutsize-1
                    varsneeded += 1
                    clsneeded += 2**(self.cutsize-1)
                else:
                    at = numlits
                    clsneeded += 2**(numlits-1)

            #in the middle
            elif at + (self.cutsize-1) < numlits :
                at += self.cutsize-2
                varsneeded += 1
                clsneeded += 2**(self.cutsize-1)
            #at the end
            else:
                clsneeded += 2**(numlits-at+1)
                at = numlits

        return [varsneeded, clsneeded]



    def get_max_var_from_infile(self, infilename) :
        infile = open(infilename, "r")

        maxvar = 0
        for line in infile:
            line = line.strip()

            #empty line, skip
            if len(line) == 0 :
                continue;

            #header or comment
            if line[0] == 'p' or line[0] == 'c':
                continue

            #print line
            maxvar = max(get_max_var(clause), maxvar)

        infile.close()

