import csv

def count_csv_lines(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        line_count = sum(1 for _ in reader)
    return line_count

# Example usage
file_path = 'data/bpf_commit.csv'  # Replace with your CSV file path
lines = count_csv_lines(file_path)
print(f'The number of lines in the CSV is: {lines}')
