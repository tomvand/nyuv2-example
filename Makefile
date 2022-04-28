all: download
.PHONY: all

download: downloads/nyu_depth_v2_labeled.mat downloads/toolbox_nyu_depth_v2.zip
.PHONY: download

clean:
	rm -r downloads || true
.PHONY: clean


downloads:
	mkdir downloads

downloads/nyu_depth_v2_labeled.mat: downloads
	curl http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat -o $@

downloads/toolbox_nyu_depth_v2.zip: downloads
	curl http://cs.nyu.edu/~silberman/code/toolbox_nyu_depth_v2.zip -o $@
