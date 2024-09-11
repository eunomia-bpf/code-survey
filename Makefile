linux:
	git clone https://github.com/torvalds/linux

bpf:
	git clone --mirror http://lore.kernel.org/bpf/0 bpf/git/0.git
	cd bpf/git/0.git && ../../../dump.sh

linux/commits.csv:
	cd linux && git log --pretty=format:'"%H","%an","%ae","%ad","%cn","%ce","%cd","%T","%P","%B"' --date=iso > commits.csv