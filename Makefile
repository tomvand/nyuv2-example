SHELL := /bin/bash

all: download unpack .venv
.PHONY: all

download: downloads/nyu_depth_v2_labeled.mat downloads/toolbox_nyu_depth_v2.zip
.PHONY: download

unpack: toolbox data/nyu_depth_v2_labeled.mat
.PHONY: unpack

clean:
	rm -r toolbox || true
	rm -r data || true
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

downloads/nyu_depth_v2_labeled.mat: | downloads
	curl -L http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat -o $@

data:
	mkdir data

data/nyu_depth_v2_labeled.mat: downloads/nyu_depth_v2_labeled.mat | data
	ln -s ../$< $@

downloads/toolbox_nyu_depth_v2.zip: | downloads
	curl -L http://cs.nyu.edu/~silberman/code/toolbox_nyu_depth_v2.zip -o $@

toolbox: downloads/toolbox_nyu_depth_v2.zip
	unzip $< -d $@
	touch $@

###########################################################

.venv: requirements.txt
	virtualenv -p python3 .venv
	source .venv/bin/activate && pip install -r requirements.txt
	touch .venv

