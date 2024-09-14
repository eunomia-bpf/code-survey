#!/bin/bash

# Run git log with the specified number of commits and format the output into a CSV file
git -C linux log --grep=bpf --pretty=format:'"%H"' > data/bpf_head_commits.csv

echo "Dumped commits to bpf_head_commits.csv"
