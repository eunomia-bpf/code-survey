linux:
	git clone https://github.com/torvalds/linux

mails/bpf:
	cd mails && git clone --mirror http://lore.kernel.org/bpf/0 bpf/git/0.git

data/feature-versions.yaml:
	wget https://raw.githubusercontent.com/isovalent/ebpf-docs/master/data/feature-versions.yaml -O data/feature-versions.yaml
