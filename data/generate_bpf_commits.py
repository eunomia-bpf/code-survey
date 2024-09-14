import csv
import subprocess
import os

# File paths
output_csv = 'data/bpf_commits.csv'

# Function to get details of a commit
def get_commit_details(commit_hash):
    result = subprocess.run(
        ['git', '-C', 'linux', 'show', '--no-patch', '--format="%H","%an","%ae","%at","%cn","%ce","%ct","%T","%P","%B"', commit_hash],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

# Function to get the list of files changed in a commit
def get_changed_files(commit_hash):
    result = subprocess.run(
        ['git', '-C', 'linux', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_hash],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip().split('\n')

# Function to check if "bpf" is in the commit message, title, or changed file paths
def contains_bpf(commit_details, changed_files):
    if 'bpf' in commit_details.lower() or any('bpf' in file.lower() for file in changed_files):
        return True
    return False

# Function to get all commit hashes
def get_all_commit_hashes():
    result = subprocess.run(
        ['git', '-C', 'linux', 'rev-list', '--all'etry],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip().split('\n')

# Function to get a list of already processed commit hashes from the CSV
def get_processed_commits(csv_file):
    if not os.path.exists(csv_file):
        return set()  # Return an empty set if the file doesn't exist

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        processed_commits = {row[0] for row in reader}  # Get all commit hashes (first column)
    return processed_commits

# Get the set of already processed commits
processed_commits = get_processed_commits(output_csv)

print("Loading all commit hashes...")
# Get all commit hashes in the repository
all_commits = get_all_commit_hashes()
print(f"Total commits: {len(all_commits)}")

# Prepare the CSV header
header = ["Commit Hash", "Author Name", "Author Email", "Author Timestamp", "Committer Name", "Committer Email", "Committer Timestamp", "Tree Hash", "Parent Hashes", "Commit Message", "Changed Files"]

# Open the CSV file in append mode
with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # If the file is newly created, write the header
    if os.path.getsize(output_csv) == 0:
        writer.writerow(header)

    # Loop through each commit and check for "bpf"
    for commit_hash in all_commits:
        # Skip already processed commits
        if commit_hash in processed_commits:
            continue

        count = str(all_commits.index(commit_hash) + 1)
        print(f"Analyzing commit {count} of {len(all_commits)}")

        # Get the commit details and changed files
        commit_details = get_commit_details(commit_hash)
        changed_files = get_changed_files(commit_hash)

        # Check if the commit contains "bpf"
        if contains_bpf(commit_details, changed_files):
            # Split commit details into fields and add the changed files
            commit_fields = commit_details.split('","')
            commit_fields[0] = commit_fields[0].strip('"')  # Clean the first field
            commit_fields[-1] = commit_fields[-1].strip('"')  # Clean the last field
            commit_fields.append(', '.join(changed_files))  # Add changed files

            # Write the commit data to the CSV
            writer.writerow(commit_fields)

print(f"Filtered 'bpf' commits saved to {output_csv}")
