import pandas as pd
import matplotlib.pyplot as plt
import os
from timeline_commits_6m import plot_frequency_timeline, get_significant_categories, apply_moving_average

# Ensure the 'imgs' directory exists
os.makedirs('imgs', exist_ok=True)

# Load the CSV file
file_path = 'data/commit_survey.csv'  # Update this with your actual file path
survey_data = pd.read_csv(file_path)

# Convert 'commit_date_timestamp' to datetime
survey_data['commit_date'] = pd.to_datetime(survey_data['commit_date_timestamp'], unit='s')

# Set 'commit_date' as the DataFrame index
survey_data.set_index('commit_date', inplace=True)

# Sort the DataFrame by date
survey_data.sort_index(inplace=True)

# Filter data to focus only on libbpf related commits
libbpf_data = survey_data[survey_data['major_related_implementation_component'].str.contains('libbpf', case=False, na=False)]

# Check how many libbpf commits are present
print(f"Total libbpf commits: {libbpf_data.shape[0]}")

# Define settings specifically for libbpf commit classifications
field_settings = {
    'commit_classification': {'title': 'libbpf Commit Classification Over Time', 'max_labels': 6, 'threshold': 0.02}
}

# Generate timeline charts for libbpf commit classifications
for field, settings in field_settings.items():
    save_path = f'imgs/timeline_libbpf_{field}_smoothed.png'
    plot_frequency_timeline(
        field_name=field,
        title=settings['title'],
        max_labels=settings['max_labels'],
        threshold=settings['threshold'],
        save_path=save_path,
        smoothing_window=4  # Adjust window size as needed
    )

print("\nlibbpf commit classification timeline chart has been saved successfully.")
