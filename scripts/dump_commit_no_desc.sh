#!/bin/bash

# Run git log with the specified number of commits and format the output into a CSV file
git -C linux log --pretty=format:'"%H","%an","%ae","%at","%cn","%ce","%ct","%T","%P","%B"' > data/all_commits_no_desc.csv

echo "Dumped commits to commits.csv"
