
DAPHNEHOME=$(HOME)/Documents/sync/progetti/Daphne
INIFILE=change_on_lemma.ini

CONLLUPATH=$(DAPHNEHOME)/data/annotation/latest/
INIPATH=$(DAPHNEHOME)/scripts/depedit/$(INIFILE)

test:
	python $(DAPHNEHOME)/scripts/depedit/test.py $(CONLLUPATH)

edit:
	python $(DAPHNEHOME)/scripts/depedit/run_depedit.py $(INIPATH) $(CONLLUPATH)

purge:
	find $(CONLLUPATH) -name "*.conllu.bak" -type f -delete