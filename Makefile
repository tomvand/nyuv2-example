SHELL := /bin/bash

all: download .venv
.PHONY: all

download: \
		toolbox \
		data/nyu_depth_v2_labeled.mat \
		data/splits.mat \
		data/nyu_depth_v1_filenames.mat \
		data/bian2022_split
.PHONY: download

clean:
	rm -r tmp || true
.PHONY: clean

purge: clean
	rm -r toolbox || true
	rm -r data || true
	rm -r .venv || true
.PHONY: purge

freeze:
	source .venv/bin/activate && pip freeze -l | grep -v "pkg_resources" > requirements.txt
.PHONY: freeze

###########################################################

tmp:
	mkdir tmp

data:
	mkdir data

data/nyu_depth_v2_labeled.mat: | data
	curl -L http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat -o $@

data/splits.mat: | data
	curl -L http://horatio.cs.nyu.edu/mit/silberman/indoor_seg_sup/splits.mat -o $@

data/nyu_depth_v1_filenames.mat: | data
	curl -L http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v1/nyu_depth_v1_filenames.mat -o $@

data/bian2022_split: | tmp data
	# curl -L https://api.onedrive.com/v1.0/shares/s!AiV6XqkxJHE2mUUA5hElvhZXnqOn/root/content -o tmp/bian2022_nyu.zip
	unzip tmp/bian2022_nyu.zip -d $@
	rm tmp/bian2022_nyu.zip
	touch $@

toolbox: | tmp
	curl -L http://cs.nyu.edu/~silberman/code/toolbox_nyu_depth_v2.zip -o tmp/toolbox_nyu_depth_v2.zip
	unzip tmp/toolbox_nyu_depth_v2.zip -d $@
	rm tmp/toolbox_nyu_depth_v2.zip
	touch $@

###########################################################

.venv: requirements.txt
	virtualenv -p python3 .venv
	source .venv/bin/activate && pip install -r requirements.txt
	touch .venv

