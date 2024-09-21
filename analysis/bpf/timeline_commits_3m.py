import pandas as pd
import matplotlib.pyplot as plt
import ast
import re
import matplotlib.dates as mdates
import os

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

# Function to safely parse the string representation of lists
# and remove "It's not related to any above" if other valid use cases exist
def parse_usecases(usecase_str):
    try:
        # Evaluate the string to convert it into a list
        usecase_list = ast.literal_eval(usecase_str)

        # Define the regex pattern for "It's not related to any above"
        pattern = re.compile(r"It's not related to any above", re.IGNORECASE)

        # Filter the list to remove "It's not related to any above" if other use cases exist
        if len(usecase_list) > 1:
            usecase_list = [usecase for usecase in usecase_list if not pattern.match(usecase)]

        return usecase_list

    except (ValueError, SyntaxError):
        # If parsing fails, return an empty list
        return []

# Apply the parsing function to the 'usecases_or_submodule_events' column
survey_data['parsed_usecases'] = survey_data['usecases_or_submodule_events'].apply(parse_usecases)

# Filter out 'merge' commits based on 'commit_classification'
# Assuming 'commit_classification' contains phrases like 'merge' and 'not related'
filter_pattern = re.compile(r'merge', re.IGNORECASE)
filtered_data = survey_data[~survey_data['commit_classification'].str.contains(filter_pattern, na=False)]

print(f"Total commits before filtering: {survey_data.shape[0]}")
print(f"Total commits after filtering out 'unrelated' and 'merge' commits: {filtered_data.shape[0]}")

# Update 'flattened_usecases' based on filtered data
flattened_usecases = pd.Series([usecase for sublist in filtered_data['parsed_usecases'] for usecase in sublist])

# Function to determine significant categories based on overall frequency
def get_significant_categories(series, max_labels, threshold=0.01):
    """
    Determine significant categories to display based on frequency threshold or max_labels.

    Parameters:
    - series: Pandas Series containing the categories.
    - max_labels: Maximum number of labels to display (including 'Other').
    - threshold: Minimum frequency proportion to consider as significant.

    Returns:
    - List of significant categories.
    """
    # Calculate frequency proportion
    freq = series.value_counts(normalize=True)

    # Determine categories above the threshold
    significant = freq[freq >= threshold].index.tolist()

    # If significant categories exceed max_labels, take the top max_labels -1 and add 'Other'
    if len(significant) > (max_labels - 1):
        significant = freq.nlargest(max_labels - 1).index.tolist()

    return significant

# Function to plot frequency-based timeline charts for categorical fields
def plot_frequency_timeline(field_name, title, max_labels, threshold, save_path):
    """
    Plot a frequency-based timeline chart for a given field.

    Parameters:
    - field_name: Column name in the DataFrame.
    - title: Title of the chart.
    - max_labels: Maximum number of labels to display (including 'Other').
    - threshold: Minimum frequency proportion to consider as significant.
    - save_path: File path to save the chart.
    """
    print(f"\nGenerating timeline for: {title}")

    # Group by 3-month intervals and category, count commits
    # '3M' stands for 3-month frequency; alternatively, you can use 'Q' for quarters
    monthly_counts = filtered_data.resample('3M')[field_name].value_counts().unstack(fill_value=0)

    # Determine significant categories
    if field_name == 'usecases_or_submodule_events':
        data_series = flattened_usecases
    else:
        data_series = filtered_data[field_name]
    significant_categories = get_significant_categories(data_series, max_labels, threshold)

    # If 'Other' needs to be added, sum the non-significant categories
    if len(significant_categories) < len(monthly_counts.columns):
        # Ensure 'Other' is not already a category
        if 'Other' not in monthly_counts.columns:
            monthly_counts['Other'] = monthly_counts.drop(significant_categories, axis=1).sum(axis=1)
        else:
            # If 'Other' exists, just sum into it
            monthly_counts['Other'] += monthly_counts.drop(significant_categories, axis=1).sum(axis=1)
        # Keep only significant categories and 'Other'
        monthly_counts = monthly_counts[significant_categories + ['Other']]

    # Plotting
    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot each category
    for column in monthly_counts.columns:
        ax.plot(monthly_counts.index, monthly_counts[column], label=column)

    # Formatting the x-axis with date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Time (3-Month Intervals)', fontsize=14)
    ax.set_ylabel('Number of Commits', fontsize=14)

    truncated_labels = [label[:20] + '...' if len(label) > 20 else label for label in monthly_counts.columns]

    ax.legend(truncated_labels, loc='upper left', bbox_to_anchor=(1,1))  # Place legend outside the plot

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"Saved timeline chart to {save_path}")

# Function to plot timeline for use cases or submodule events
def plot_usecases_timeline(title, save_path, max_labels=8, threshold=0.005):
    """
    Plot a frequency-based timeline chart for use cases or submodule events.

    Parameters:
    - title: Title of the chart.
    - save_path: File path to save the chart.
    - max_labels: Maximum number of labels to display (including 'Other').
    - threshold: Minimum frequency proportion to consider as significant.
    """
    print(f"\nGenerating timeline for: {title}")

    # Explode the 'parsed_usecases' lists into separate rows
    exploded_data = filtered_data.explode('parsed_usecases')

    # Remove "not related" cases
    filter_pattern = re.compile(r'not relate', re.IGNORECASE)
    exploded_data = exploded_data[~exploded_data['parsed_usecases'].str.contains(filter_pattern, na=False)]

    # Remove NaN entries
    exploded_data = exploded_data.dropna(subset=['parsed_usecases'])

    # Group by 3-month intervals and use case, count commits
    monthly_counts = exploded_data.resample('3M')['parsed_usecases'].value_counts().unstack(fill_value=0)

    # Determine significant categories
    significant_categories = get_significant_categories(flattened_usecases, max_labels, threshold)

    # Only drop categories that exist in the DataFrame
    columns_to_drop = [col for col in monthly_counts.columns if col not in significant_categories]

    # If 'Other' needs to be added, sum the non-significant categories
    if len(columns_to_drop) > 0:
        # Add 'Other' column as the sum of non-significant categories
        monthly_counts['Other'] = monthly_counts[columns_to_drop].sum(axis=1)
        monthly_counts = monthly_counts.drop(columns=columns_to_drop, axis=1)

    # Plotting
    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot each category
    for column in monthly_counts.columns:
        ax.plot(monthly_counts.index, monthly_counts[column], label=column)

    # Formatting the x-axis with date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Time (3-Month Intervals)', fontsize=14)
    ax.set_ylabel('Number of Commits', fontsize=14)

    # Truncate long labels for the legend
    truncated_labels = [label[:20] + '...' if len(label) > 20 else label for label in monthly_counts.columns]

    # Add the legend with truncated labels
    ax.legend(truncated_labels, loc='upper left', bbox_to_anchor=(1, 1))  # Place legend outside the plot

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"Saved timeline chart to {save_path}")

# Define thresholds and max_labels per field
field_settings = {
    'commit_classification': {'title': 'Commit Classification Over Time', 'max_labels': 6, 'threshold': 0.02},
    'commit_complexity': {'title': 'Commit Complexity Over Time', 'max_labels': 4, 'threshold': 0.05},
    'major_related_implementation_component': {'title': 'Major Implementation Component Over Time', 'max_labels': 8, 'threshold': 0.01},
    'major_related_logic_component': {'title': 'Major Logic Component Over Time', 'max_labels': 8, 'threshold': 0.01},
}

# Generate timeline charts for categorical fields
for field, settings in field_settings.items():
    save_path = f'imgs/timeline_{field}.png'
    plot_frequency_timeline(
        field_name=field,
        title=settings['title'],
        max_labels=settings['max_labels'],
        threshold=settings['threshold'],
        save_path=save_path
    )

# Generate timeline chart for use cases or submodule events
plot_usecases_timeline(
    title='Use Cases or Submodule Events Over Time',
    save_path='imgs/timeline_usecases_or_submodule_events.png',
    max_labels=12,
    threshold=0.005  # Adjusted threshold for more use cases
)

print("\nAll timeline charts have been saved successfully.")
