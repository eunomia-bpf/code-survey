#!/bin/bash

# Create CSV header
echo '"Commit Hash","Author Name","Author Email","Author Timestamp","Committer Name","Committer Email","Committer Timestamp","Tree Hash","Parent Hashes","Commit Message","Notes"' > data/all_commits.csv

# Run git log with the specified number of commits and format the output into the CSV file
git -C linux log --pretty=format:'"%H","%an","%ae","%at","%cn","%ce","%ct","%T","%P","%B","%N"' >> data/all_commits.csv

echo "Dumped commits to commits.csv"
