import subprocess
import pandas as pd
import csv

# Function to run the bash command to generate the commit list
def generate_commit_list():
    bash_command = 'git -C linux log --grep=bpf --pretty=format:%H'  # No quotes around %H
    result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr or result.stdout}")
        return []
    commit_ids = result.stdout.strip().split('\n')
    print(f"Generated {len(commit_ids)} commit IDs")
    return commit_ids

# Function to get commit details using git show
def get_commit_details(commit_id):
    command = [
        'git', '-C', 'linux', 'show', commit_id, 
        '--pretty=format:%H,%an,%ae,%at,%cn,%ce,%ct,%T,%P',  # No quotes here either
        '--no-patch'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr or result.stdout}")
        return []
    return result.stdout.strip().split(',')

# Function to get commit message
def get_commit_message(commit_id):
    command = ['git', '-C', 'linux', 'show', '-s', '--pretty=%B', commit_id]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr or result.stdout}")
        return ""
    return result.stdout.strip().replace("\n", " ")  # Replace newlines to avoid splitting into multiple columns

# Function to get the list of files changed in a commit
def get_changed_files(commit_hash):
    result = subprocess.run(
        ['git', '-C', 'linux', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_hash],
        stdout=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        print(f"Error getting changed files for {commit_hash}: {result.stderr or result.stdout}")
        return []
    return result.stdout.strip().split('\n')

# Function to write commit details into a CSV using pandas
def write_to_csv_pandas(data, csv_file):
    df = pd.DataFrame(data, columns=["commit_id", "commit_hash", "author_name", "author_email", 
                                     "author_date", "committer_name", "committer_email", 
                                     "commit_date_timestamp", "tree_hash", "parent_hashes", 
                                     "commit_message", "changed_files"])
    df.to_csv(csv_file, index=False, quoting=csv.QUOTE_ALL)

# Function to process commit IDs and generate a new CSV with commit details and changed files using pandas
def process_commits_and_generate_csv(output_csv):
    # Step 1: Generate commit IDs
    commit_ids = generate_commit_list()
    
    if not commit_ids:
        print("No commits found. Exiting.")
        return

    data = []
    total_commits = len(commit_ids)  # Get total number of commits for progress tracking
    
    # Step 2: Get details for each commit and changed files
    for count, commit_id in enumerate(commit_ids, 1):  # Start counter from 1
        print(f"Processing {count}/{total_commits}...")  # Show the current progress
        commit_details = get_commit_details(commit_id)
        if len(commit_details) != 9:  # Ensure all 9 columns are present
            print(f"Warning: Incomplete data for commit {commit_id}, skipping.")
            continue
        
        changed_files = get_changed_files(commit_id)
        commit_message = get_commit_message(commit_id)  # Fetch the commit message separately
        
        # Ensure that commit_message and changed_files are not empty
        if not commit_message:
            commit_message = "No commit message"
        if not changed_files:
            changed_files = ["No changed files"]

        # Append the commit_message and changed_files columns to commit details
        commit_details.append(commit_message)
        commit_details.append(";".join(changed_files))  # Join file names with semicolons for CSV

        if len(commit_details) != 11:  # Ensure 11 columns (9 from details + 2 more we added)
            print(f"Error: Mismatch in column count for commit {commit_id}.")
            continue

        # Add commit ID to the beginning (to make 12 columns total)
        data.append([commit_id] + commit_details)

    # Step 3: Write the commit details to the CSV using pandas
    write_to_csv_pandas(data, output_csv)

# Example usage
output_csv = 'data/bpf_commits.csv'  # Path to the output CSV file

if __name__ == '__main__':
    process_commits_and_generate_csv(output_csv)
