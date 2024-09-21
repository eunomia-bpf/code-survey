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
    'helpers': 'helper/kfunc',
    'kfuncs': 'helper/kfunc',
    'sock_ops': 'events',
    'sock_opt_types': 'events',
    'link_type': 'links',
    'attach_types': 'events'
})

# Remove 'argument_constants' and 'helper/kfunc'
df = df[(df['feature_type'] != 'argument_constants') & (df['feature_type'] != 'helper/kfunc')]

# Sort values by date to maintain order in cumulative calculation
df_sorted = df.sort_values(by='author_date')

# Group by date and feature type, sum counts, and calculate cumulative sum
df_cumulative_fixed = df_sorted.groupby(['author_date', 'feature_type'])['count'].sum().groupby(level=1).cumsum().unstack(fill_value=0)

# Ensure cumulative sums are consistent and avoid resetting to zero
df_cumulative_fixed = df_cumulative_fixed.cummax()

# Plot the cumulative count of features over time, grouped by feature type
plt.figure(figsize=(8, 5))
df_cumulative_fixed.plot(ax=plt.gca())

plt.title('Cumulative BPF Features Commit Timeline without Helper/Kfunc')
plt.xlabel('Date')
plt.ylabel('Cumulative Count of Features')
plt.legend(title='Feature Type')
plt.grid(True)
plt.tight_layout()

# Save the plot to the current directory
plt.savefig('imgs/cumulative_bpf_features_timeline_no_helper_kfunc.png')

plt.show()
