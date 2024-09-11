.PHONY: linux mails/bpf data/feature-versions.yaml agent/questionaire
linux:
	git clone https://github.com/torvalds/linux

mails/bpf:
	cd mails && git clone --mirror http://lore.kernel.org/bpf/0 bpf/git/0.git

data/feature-versions.yaml:
	wget https://raw.githubusercontent.com/isovalent/ebpf-docs/master/data/feature-versions.yaml -O data/feature-versions.yaml

agent/questionaire:
	python -m datamodel_code_generator --input agent/questionaire.yml --input-file-type jsonschema --output agent/model.py --use-schema-description --use-default
