import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'data/feature_commit_details.csv'
df = pd.read_csv(file_path)

# Convert the author_date column from Unix timestamp to datetime
df['author_date'] = pd.to_datetime(df['author_date'], unit='s', errors='coerce')

# Create a new 'count' column to facilitate the cumulative count
df['count'] = 1

# Keep only the specific four feature types
df['feature_type'] = df['feature_type'].replace({
    'sock_ops': 'sock_ops',
    'sock_opt_types': 'sock_opt_types',
    'link_type': 'link_type',
    'attach_types': 'attach_types'
})

# Filter the data to include only 'sock_ops', 'sock_opt_types', 'link_type', and 'attach_types'
df_filtered = df[df['feature_type'].isin(['sock_ops', 'sock_opt_types', 'link_type', 'attach_types'])]

# Sort values by date to maintain order in cumulative calculation
df_sorted = df_filtered.sort_values(by='author_date')

# Group by date and feature type, sum counts, and calculate cumulative sum
df_cumulative_fixed = df_sorted.groupby(['author_date', 'feature_type'])['count'].sum().groupby(level=1).cumsum().unstack(fill_value=0)

# Ensure cumulative sums are consistent and avoid resetting to zero
df_cumulative_fixed = df_cumulative_fixed.cummax()

# Create a date range that spans from the earliest to the latest commit date
full_date_range = pd.date_range(start=df['author_date'].min(), end=df['author_date'].max())

# Reindex the cumulative data to ensure all dates are included
df_cumulative_fixed = df_cumulative_fixed.reindex(full_date_range, method='ffill', fill_value=0)

# Plot the cumulative count of the four selected feature types over time
plt.figure(figsize=(8, 5))
for feature_type in ['sock_ops', 'sock_opt_types', 'link_type', 'attach_types']:
    plt.plot(df_cumulative_fixed.index, df_cumulative_fixed[feature_type], label=feature_type)

plt.title('Cumulative BPF Features: sock_ops, sock_opt_types, link_type, attach_types')
plt.xlabel('Date')
plt.ylabel('Cumulative Count of Features')
plt.legend(title='Feature Type')
plt.grid(True)
plt.tight_layout()

# Save the plot to a file
plt.savefig('imgs/cumulative_sock_link_features_timeline.png')

plt.show()
