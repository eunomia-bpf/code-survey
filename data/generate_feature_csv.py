import yaml
import subprocess
import csv

# Function to load YAML file
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to get commit details using git show
def get_commit_details(commit_id):
    command = [
        'git', '-C', '../linux', 'show', commit_id, 
        '--pretty=format:"%H","%an","%ae","%at","%cn","%ce","%ct","%T","%P","%B","%N"',
        '--no-patch'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr or result.stdout}")
        return
    print(f"Processed commit: {commit_id}") # Print commit id to track progress
    return result.stdout

# Function to write commit details into a CSV
def write_to_csv(data, csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["commit_id", "feature_type", "feature_name", "commit_hash", "author_name", "author_email", "author_date",
                         "committer_name", "committer_email", "commit_date_timestamp", "tree_hash", "parent_hashes", "commit_message", "refs"])

        for row in data:
            writer.writerow(row)

# Function to process YAML and collect commit info
def process_yaml_and_generate_csv(yaml_file, csv_file):
    data = load_yaml(yaml_file)
    csv_data = []
    
    for feature_type in data:
        for feature in feature_type['features']:
            commit_id = feature['commit']
            commit_info = get_commit_details(commit_id)
            commit_details = commit_info.strip('"').split('","')
            csv_data.append([commit_id, feature_type['name'], feature['name']] + commit_details)
    
    write_to_csv(csv_data, csv_file)

# Example usage
yaml_file = 'feature-versions.yaml'
csv_output_file = 'feature_commit_details.csv'

if __name__ == '__main__':
    process_yaml_and_generate_csv(yaml_file, csv_output_file)