import csv

def process_commits_csv(file_path):
    # Open the CSV file for reading
    with open(file_path, mode='r', encoding='utf-8') as file:
        # Use csv.reader to parse the CSV file
        csv_reader = csv.reader(file)
        
        # Define headers for better understanding of what each column represents
        headers = ["commit_hash", "author_name", "author_email", "author_date", 
                   "committer_name", "committer_email", "committer_date", 
                   "tree_hash", "parent_hashes", "full_commit_message"]
        
        # Initialize an empty list to store processed commits
        commits = []

        # Process each row in the CSV
        for row in csv_reader:
            # Ensure that the row is correctly formatted
            if len(row) == len(headers):
                commit_data = dict(zip(headers, row))
                commits.append(commit_data)

        return commits

if __name__ == "__main__":
    # Path to your CSV file
    file_path = 'commits.csv'

    # Process the CSV file
    commits = process_commits_csv(file_path)

    # Print out a summary of the commits
    # print_commit_summary(commits)

    # You can further process `commits` list as needed (e.g., filter by author, date, etc.)
