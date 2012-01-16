CXXFLAGS := -Wall -g -O3

programs := \
	cnf-cat \
	cnf-clause \
	cnf-grep \
	cnf-shuffle-variables \
	cnf-shuffle-literals \
	cnf-shuffle-clauses \
	cnf-sort-literals \
	cnf-sort-clauses \
	cnf-propagate \
	cnf-stat \
	cnf-complete \
	cnf-renumber \
	cnf-fuzz

all: $(programs)

clean:
	rm -rf $(programs)
