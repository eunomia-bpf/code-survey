import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Ensure the 'imgs' directory exists to save output if needed
os.makedirs('imgs', exist_ok=True)

# Load the CSV file
file_path = 'data/commit_survey.csv' # Replace with your actual file path
survey_data = pd.read_csv(file_path)

# Convert 'commit_date_timestamp' to datetime
survey_data['commit_date'] = pd.to_datetime(survey_data['commit_date_timestamp'], unit='s')

# Set 'commit_date' as the DataFrame index
survey_data.set_index('commit_date', inplace=True)

# Sort the DataFrame by date
survey_data.sort_index(inplace=True)

# Filter the dataset to include libbpf-related commits
libbpf_data = survey_data[survey_data['major_related_implementation_component'].str.contains('libbpf', case=False, na=False)]

# Get unique classifications related to libbpf
libbpf_classifications = libbpf_data['commit_classification'].unique()

# Plot for each classification, with shorter labels
plt.figure(figsize=(10, 6))

for classification in libbpf_classifications:
    # Filter data for the current classification
    classification_data = libbpf_data[libbpf_data['commit_classification'].str.contains(classification, case=False, na=False)]
    
    # Resample the data by 6-month intervals and count the number of commits for this classification
    classification_counts = classification_data.resample('6M').size()
    
    # Shorten classification label to 20 characters
    short_label = classification[:20] + '...' if len(classification) > 20 else classification
    
    # Plot the evolution of libbpf for the current classification
    plt.plot(classification_counts.index, classification_counts.values, label=short_label)

# Formatting the x-axis with date labels
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gcf().autofmt_xdate()

# Add title and labels
# plt.title('Evolution and Status of libbpf by Commit Classification (Short Labels)', fontsize=16)
plt.xlabel('Time (6-Month Intervals)', fontsize=14)
plt.ylabel('Number of Commits', fontsize=14)

# Add legend and grid
plt.legend(title='Commit Classification', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.savefig('imgs/libbpf_evolution_by_classification.png')
