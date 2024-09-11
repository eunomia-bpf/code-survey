#!/bin/bash

# Create the emails directory if it doesn't exist
mkdir -p emails

# Get all the objects ending with 'm' from the git history
git -C mails/bpf/git/0.git rev-list --all --objects | grep 'm$' | awk '{print $1}' | while read commit_id; do
    # Output the content of the commit to a file named after the commit id in the emails/ directory
    git -C mails/bpf/git/0.git cat-file -p $commit_id > "emails/${commit_id}.txt"
done
