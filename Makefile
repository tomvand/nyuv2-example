SHELL := /bin/bash

all: download .venv
.PHONY: all

download: downloads/nyu_depth_v2_labeled.mat downloads/toolbox_nyu_depth_v2.zip
.PHONY: download

clean:
.PHONY: clean

purge: clean
	rm -r downloads || true
	rm -r .venv || true
.PHONY: purge

freeze:
	source .venv/bin/activate && pip freeze -l | grep -v "pkg_resources" > requirements.txt
.PHONY: freeze

###########################################################

downloads:
	mkdir downloads

downloads/nyu_depth_v2_labeled.mat: downloads
	curl http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat -o $@

downloads/toolbox_nyu_depth_v2.zip: downloads
	curl http://cs.nyu.edu/~silberman/code/toolbox_nyu_depth_v2.zip -o $@

###########################################################

.venv: requirements.txt
	virtualenv -p python3 .venv
	source .venv/bin/activate && pip install -r requirements.txt
	touch .venv

