/*  cnf-propagate Copyright (c) 2011, Vegard Nossum
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

extern "C" {
#include <stdio.h>
#include <stdlib.h>
}

#include <algorithm>
#include <map>
#include <set>

#include "cnf.hh"

class literal_eq {
public:
	cnf::literal x;

	literal_eq(cnf::literal x):
		x(x)
	{
	}

	bool operator()(cnf::literal y)
	{
		return x == y;
	}
};

int main(int argc, char *argv[])
{
	FILE *fp;
	if (argc > 1) {
		fp = fopen(argv[1], "r");
		/* XXX: Real error checking */
		assert(fp);
	} else {
		fp = stdin;
	}

	unsigned int nr_variables;
	unsigned int nr_clauses;
	if (fscanf(fp, "p cnf %u %u\n", &nr_variables, &nr_clauses) != 2) {
		fprintf(stderr, "error: expected: p cnf <variables> <clauses>\n");
		exit(EXIT_FAILURE);
	}

	typedef std::set<cnf::clause::ptr> clause_set;
	typedef std::map<cnf::literal, clause_set> literal_map;

	literal_map map;

	typedef std::set<cnf::literal> literal_set;

	literal_set agenda;

	cnf f;
    start:
	for (unsigned int i = 0; i < nr_clauses; ++i) {
		cnf::clause::ptr clause(new cnf::clause());

		while (1) {
			int literal;
			if (fscanf(fp, "%d", &literal) != 1) {
                if (i == 0) {
                    char c;
                    fscanf(fp, "%c", &c);
                    if (c == 'c') {
                        while(c != '\n') {
                            fscanf(fp, "%c", &c);
                        }
                        goto start;
                    }
                }

				fprintf(stderr, "error: expected literal\n");
				exit(EXIT_FAILURE);
			}

			if (!literal)
				break;

			clause->add(literal);
			map[literal].insert(clause);
		}

		f.add(clause);
		if (clause->literals.size() == 1)
			agenda.insert(clause->literals[0]);
	}

	while (agenda.size()) {
		literal_set::iterator it = agenda.begin();
		cnf::literal literal = *it;
		agenda.erase(it);

		literal_map::iterator lit;
		if ((lit = map.find(-literal)) != map.end()) {
			clause_set &clauses = lit->second;
			for (clause_set::iterator cit = clauses.begin(),
				cend = clauses.end(); cit != cend; ++cit)
			{
				cnf::clause::ptr clause(*cit);

				/* Leave unit clauses in the formula */
				if (clause->literals.size() == 1)
					continue;

				clause->literals.erase(std::remove_if(clause->literals.begin(), clause->literals.end(), literal_eq(-literal)), clause->literals.end());

				/* Propagate again */
				if (clause->literals.size() == 1)
					agenda.insert(clause->literals[0]);
			}
		}

		if ((lit = map.find(literal)) != map.end()) {
			clause_set &clauses = lit->second;
			for (clause_set::iterator cit = clauses.begin(),
				cend = clauses.end(); cit != cend; ++cit)
			{
				cnf::clause::ptr clause(*cit);

				/* Leave unit clauses alone (XXX: Can this ever happen?) */
				if (clause->literals.size() == 1)
					continue;

				/* Remove the clause by making it a tautology */
				clause->literals.push_back(-literal);
			}
		}
	}

	printf("p cnf %u %u\n", nr_variables, nr_clauses);
	f.print(stdout);

	fclose(fp);
	return 0;
}
