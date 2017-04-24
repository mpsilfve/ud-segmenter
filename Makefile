PYTHON=/usr/local/bin/pypy3

all:eval

results/%test.sys:data/%train+test data/%test
	$(PYTHON) base_sample.py $^ > $@

eval:results/fitest.sys results/svtest.sys results/estest.sys
	echo "FINNISH"
	$(PYTHON) eval.py results/fitest.sys data/fitest.gold
	echo "SWEDISH"
	$(PYTHON) eval.py results/svtest.sys data/svtest.gold
	echo "SPANISH"
	$(PYTHON) eval.py results/estest.sys data/estest.gold