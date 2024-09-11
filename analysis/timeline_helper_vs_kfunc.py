import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'data/feature_commit_details.csv'
df = pd.read_csv(file_path)

# Convert the author_date column from Unix timestamp to datetime
df['author_date'] = pd.to_datetime(df['author_date'], unit='s', errors='coerce')

# Create a new 'count' column to facilitate the cumulative count
df['count'] = 1

# Group similar feature types: merge `helpers/kfunc`, `socket/link/attach`
df['feature_type'] = df['feature_type'].replace({
    'sock_ops': 'socket',
    'sock_opt_types': 'socket',
    'link_type': 'link/attach',
    'attach_types': 'link/attach'
})

# Remove argument_constants
df = df[df['feature_type'] != 'argument_constants']

# Sort values by date to maintain order in cumulative calculation
df_sorted = df.sort_values(by='author_date')

# Group by date and feature type, sum counts, and calculate cumulative sum
df_cumulative_fixed = df_sorted.groupby(['author_date', 'feature_type'])['count'].sum().groupby(level=1).cumsum().unstack(fill_value=0)

# Ensure cumulative sums are consistent and avoid resetting to zero
df_cumulative_fixed = df_cumulative_fixed.cummax()

# Filter the data for 'helper' and 'kfunc' separately
df_helper_kfunc = df_sorted[df_sorted['feature_type'].isin(['helpers', 'kfuncs'])]

# Separate 'helper' and 'kfunc' for individual cumulative counts
df_helper = df_helper_kfunc[df_helper_kfunc['feature_type'] == 'helpers']
df_kfunc = df_helper_kfunc[df_helper_kfunc['feature_type'] == 'kfuncs']

# Create cumulative sums for each
df_helper_cumulative = df_helper.groupby(['author_date'])['count'].sum().cumsum()
df_kfunc_cumulative = df_kfunc.groupby(['author_date'])['count'].sum().cumsum()

# Create a date range that spans from the earliest to the latest commit date
full_date_range = pd.date_range(start=df['author_date'].min(), end=df['author_date'].max())

# Reindex the cumulative data to ensure all dates are included
df_helper_cumulative = df_helper_cumulative.reindex(full_date_range, method='ffill', fill_value=0)
df_kfunc_cumulative = df_kfunc_cumulative.reindex(full_date_range, method='ffill', fill_value=0)

# Plot the cumulative count of 'helper' and 'kfunc' over time
plt.figure(figsize=(10, 6))
plt.plot(df_helper_cumulative.index, df_helper_cumulative.values, label='Helper')
plt.plot(df_kfunc_cumulative.index, df_kfunc_cumulative.values, label='Kfunc', linestyle='--')

plt.title('Cumulative BPF Features: Helper vs Kfunc')
plt.xlabel('Date')
plt.ylabel('Cumulative Count of Features')
plt.legend(title='Feature Type')
plt.grid(True)
plt.tight_layout()

# Save the plot to a file
plt.savefig('imgs/cumulative_helper_kfunc_timeline.png')

plt.show()
