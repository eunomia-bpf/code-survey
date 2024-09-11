#!/bin/bash

# Run git log with the specified number of commits and format the output into a CSV file
git -C ../linux log --pretty=format:'"%H","%an","%ae","%ad","%cn","%ce","%cd","%T","%P","%B","%N"' --date=iso > commits.csv

echo "Dumped commits to commits.csv"
