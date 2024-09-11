#!/bin/bash

# Check if the number of commits (n) is passed as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <number_of_commits>"
  exit 1
fi

# Store the argument in a variable
n=$1

# Run git log with the specified number of commits and format the output into a CSV file
git log --pretty=format:'"%H","%an","%ae","%ad","%cn","%ce","%cd","%T","%P","%B","%N"' -n "$n" --date=iso > commits.csv

echo "Dumped $n commits to commits.csv"
