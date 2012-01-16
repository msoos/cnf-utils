/*  cnf-utils  Copyright (c) 2011, Vegard Nossum
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef CNF_HH
#define CNF_HH

#include <boost/shared_ptr.hpp>

#include <vector>

class cnf {
public:
	typedef int literal;

	class clause {
	public:
		typedef boost::shared_ptr<clause> ptr;
		typedef std::vector<literal> literal_vector;

		literal_vector literals;

		clause()
		{
		}

		void add(literal x)
		{
			literals.push_back(x);
		}
	};

	typedef std::vector<clause::ptr> clause_vector;

	clause_vector clauses;

	cnf()
	{
	}

	void add(clause::ptr c)
	{
		clauses.push_back(c);
	}

	void print(FILE *fp)
	{
        std::vector<char> litsInside;
		for (clause_vector::iterator cit = clauses.begin(),
			cend = clauses.end(); cit != cend; ++cit)
		{
			clause::ptr c(*cit);


            litsInside.clear();
            bool isSAT = false;
            for (clause::literal_vector::iterator lit = c->literals.begin(),
                lend = c->literals.end(); lit != lend; ++lit)
            {
                unsigned at = std::abs(*lit)*2;
                unsigned atother = at;
                if (*lit > 0) {
                    at += 1;
                } else {
                    atother += 1;
                }

                if (litsInside.size() < at)
                    litsInside.resize(at+1, 0);

                if (litsInside[atother]) {
                    isSAT = true;
                }
                litsInside[at] = 1;
            }

            if (!isSAT) {
                for (clause::literal_vector::iterator lit = c->literals.begin(),
                    lend = c->literals.end(); lit != lend; ++lit)
                {
                    fprintf(fp, "%d ", *lit);
                }

                fprintf(fp, "0\n");
            }
		}
	}
};

#endif
