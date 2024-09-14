import subprocess
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
        '--pretty=format:%H,%an,%ae,%at,%cn,%ce,%ct,%T,%P,%B,%N',  # No quotes here either
        '--no-patch'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr or result.stdout}")
        return []
    print(f"Processed commit: {commit_id}")  # Print commit id to track progress
    return result.stdout.strip().split(',')

# Function to write commit details into a CSV
def write_to_csv(data, csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["commit_id", "commit_hash", "author_name", "author_email", "author_date",
                         "committer_name", "committer_email", "commit_date_timestamp", "tree_hash", 
                         "parent_hashes", "commit_message", "refs"])

        for row in data:
            writer.writerow(row)

# Function to process commit IDs and generate a new CSV with commit details
def process_commits_and_generate_csv(output_csv):
    # Step 1: Generate commit IDs
    commit_ids = generate_commit_list()
    
    if not commit_ids:
        print("No commits found. Exiting.")
        return

    csv_data = []
    
    # Step 2: Get details for each commit
    for commit_id in commit_ids:
        commit_details = get_commit_details(commit_id)
        if commit_details:
            csv_data.append([commit_id] + commit_details)

    # Step 3: Write the commit details to the CSV
    write_to_csv(csv_data, output_csv)

# Example usage
output_csv = 'data/bpf_commits.csv'  # Path to the output CSV file

if __name__ == '__main__':
    process_commits_and_generate_csv(output_csv)
