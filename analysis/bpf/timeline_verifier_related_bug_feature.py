import pandas as pd
import matplotlib.pyplot as plt

# Load the data (assuming you have a CSV file with the same structure)
data = pd.read_csv('data/commit_survey.csv')

# Step 1: Convert 'commit_date_timestamp' to 'commit_date' if needed
if 'commit_date_timestamp' in data.columns:
    data['commit_date'] = pd.to_datetime(data['commit_date_timestamp'], unit='s')
else:
    data['commit_date'] = pd.to_datetime(data['commit_date'])

# Step 2: Filter commits related to verifier component within instruction logic
verifier_instruction_features = data[
    data['major_related_logic_component'].str.contains('instruction', case=False, na=False) &
    data['major_related_implementation_component'].str.contains('verifier', case=False, na=False)
].copy()

# Step 3: Categorize verifier instruction commits as 'feature'
verifier_instruction_features = verifier_instruction_features[
    ~verifier_instruction_features['commit_classification'].str.contains('bug', case=False, na=False)
]

# Step 4: Filter general bugs related to verifier but not instruction
general_bugs = data[
    data['major_related_implementation_component'].str.contains('verifier', case=False, na=False) &
    data['commit_classification'].str.contains('bug', case=False, na=False)
].copy()

# Step 5: Group verifier instruction features by month
verifier_features_over_time = verifier_instruction_features.groupby(
    verifier_instruction_features['commit_date'].dt.to_period('M')
).size().reset_index(name='verifier_features')

# Step 6: Group general bugs by month
general_bugs_over_time = general_bugs.groupby(
    general_bugs['commit_date'].dt.to_period('M')
).size().reset_index(name='general_bugs')

# Step 7: Merge the two datasets on the commit_date
merged_data = pd.merge(
    verifier_features_over_time,
    general_bugs_over_time,
    on='commit_date',
    how='outer'
).fillna(0)

# Step 8: Convert 'commit_date' back to timestamp for plotting
merged_data['commit_date'] = merged_data['commit_date'].dt.to_timestamp()

# Step 9: Sort the data by commit_date
merged_data = merged_data.sort_values('commit_date')

# Step 10: Plot the comparison
plt.figure(figsize=(10, 6))

plt.plot(
    merged_data['commit_date'],
    merged_data['verifier_features'],
    marker='s',
    label='Verifier Instruction Features',
    color='blue'
)
plt.plot(
    merged_data['commit_date'],
    merged_data['general_bugs'],
    marker='x',
    label='General Verifier Bugs',
    color='red'
)

# Add titles and labels
plt.title('Verifier Instruction Modification vs. General Verifier Bugs Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Commits')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as an image
plt.savefig("imgs/verifier_features_vs_general_bugs_over_time.png")

# Show the plot
plt.show()
