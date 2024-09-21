import pandas as pd
import matplotlib.pyplot as plt
import ast
import re
import matplotlib.dates as mdates
import os
import warnings

# Optionally suppress FutureWarnings (not recommended for production)
# warnings.simplefilter(action='ignore', category=FutureWarning)

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

# Filter out 'merge' commits based on 'major_related_implementation_component'
# because some important commits might be classified as 'merge' in classification, but it's related to the major component
# Assuming 'commit_classification' contains phrases like 'merge' and 'not related'
filter_pattern = re.compile(r'merge', re.IGNORECASE)
filtered_data = survey_data[~survey_data['major_related_implementation_component'].str.contains(filter_pattern, na=False)]

print(f"Total commits before filtering: {survey_data.shape[0]}")
print(f"Total commits after filtering out 'unrelated' and 'merge' commits: {filtered_data.shape[0]}")

# Update 'flattened_usecases' based on filtered data, excluding "not related" strings
flattened_usecases = pd.Series([
    usecase for sublist in filtered_data['parsed_usecases'] for usecase in sublist
    if not re.search(r"not relate", usecase, re.IGNORECASE)
])

# Debug: Check the contents of flattened_usecases
print(f"Number of use cases after exclusion: {len(flattened_usecases)}")
print(f"Sample use cases:\n{flattened_usecases.head()}")

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

# Function to apply moving average
def apply_moving_average(df, window=2):
    """
    Apply moving average to each column in the DataFrame.

    Parameters:
    - df: Pandas DataFrame with numeric data.
    - window: Window size for the moving average.

    Returns:
    - Pandas DataFrame with smoothed data.
    """
    return df.rolling(window=window, min_periods=1).mean()

# Function to plot frequency-based timeline charts for categorical fields with smoothing
def plot_frequency_timeline(field_name, title, max_labels, threshold, save_path, smoothing_window=2):
    """
    Plot a frequency-based timeline chart for a given field with smoothing.

    Parameters:
    - field_name: Column name in the DataFrame.
    - title: Title of the chart.
    - max_labels: Maximum number of labels to display (including 'Other').
    - threshold: Minimum frequency proportion to consider as significant.
    - save_path: File path to save the chart.
    - smoothing_window: Window size for moving average.
    """
    print(f"\nGenerating timeline for: {title}")

    # Group by 6-month intervals and category, count commits
    # Changed '6M' to '3MS' to align with possible deprecation
    monthly_counts = filtered_data.resample('3MS')[field_name].value_counts().unstack()

    # Determine significant categories
    if field_name == 'usecases_or_submodule_events':
        data_series = flattened_usecases
    else:
        data_series = filtered_data[field_name]
    significant_categories = get_significant_categories(data_series, max_labels, threshold)

    # Debug: Print significant categories
    print(f"Significant Categories for {field_name}: {significant_categories}")

    # If 'Other' needs to be added, sum the non-significant categories
    if len(significant_categories) < len(monthly_counts.columns):
        # Ensure 'Other' is not already a category
        non_significant = monthly_counts.columns.difference(significant_categories)
        if 'Other' not in monthly_counts.columns:
            # Sum non-significant categories, treating NaNs as 0
            monthly_counts['Other'] = monthly_counts[non_significant].sum(axis=1, skipna=True)
        else:
            # If 'Other' exists, just sum into it
            monthly_counts['Other'] += monthly_counts[non_significant].sum(axis=1, skipna=True)
        # Keep only significant categories and 'Other'
        monthly_counts = monthly_counts[significant_categories + ['Other']]

    # Apply moving average for smoothing
    smoothed_counts = apply_moving_average(monthly_counts, window=smoothing_window)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each category
    for column in smoothed_counts.columns:
        ax.plot(smoothed_counts.index, smoothed_counts[column], label=column)

    # Formatting the x-axis with date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Time (6-Month Intervals)', fontsize=14)
    ax.set_ylabel('Number of Commits (Smoothed)', fontsize=14)

    truncated_labels = [label[:20] + '...' if len(label) > 20 else label for label in smoothed_counts.columns]

    ax.legend(truncated_labels, loc='upper left', bbox_to_anchor=(1,1))  # Place legend outside the plot

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"Saved smoothed timeline chart to {save_path}")

# Function to plot timeline for use cases or submodule events with smoothing
def plot_usecases_timeline(title, save_path, max_labels=8, threshold=0.005, smoothing_window=2):
    """
    Plot a frequency-based timeline chart for use cases or submodule events with smoothing.

    Parameters:
    - title: Title of the chart.
    - save_path: File path to save the chart.
    - max_labels: Maximum number of labels to display (including 'Other').
    - threshold: Minimum frequency proportion to consider as significant.
    - smoothing_window: Window size for moving average.
    """
    print(f"\nGenerating timeline for: {title}")

    # Explode the 'parsed_usecases' lists into separate rows
    exploded_data = filtered_data.explode('parsed_usecases')

    # Remove "not related" cases
    filter_pattern = re.compile(r'not relate', re.IGNORECASE)
    exploded_data = exploded_data[~exploded_data['parsed_usecases'].str.contains(filter_pattern, na=False)]

    # Remove NaN entries
    exploded_data = exploded_data.dropna(subset=['parsed_usecases'])

    # Group by 6-month intervals and use case, count commits
    # Changed '6M' to '3MS' to align with possible deprecation
    monthly_counts = exploded_data.resample('3MS')['parsed_usecases'].value_counts().unstack()

    # Determine significant categories
    significant_categories = get_significant_categories(flattened_usecases, max_labels, threshold)

    # Debug: Print significant categories
    print(f"Significant Categories for Use Cases: {significant_categories}")

    # If 'Other' needs to be added, sum the non-significant categories
    if len(significant_categories) < len(monthly_counts.columns):
        # Identify non-significant categories
        non_significant = monthly_counts.columns.difference(significant_categories)
        if 'Other' not in monthly_counts.columns:
            # Sum non-significant categories, treating NaNs as 0
            monthly_counts['Other'] = monthly_counts[non_significant].sum(axis=1, skipna=True)
        else:
            # If 'Other' exists, just sum into it
            monthly_counts['Other'] += monthly_counts[non_significant].sum(axis=1, skipna=True)
        # Keep only significant categories and 'Other'
        monthly_counts = monthly_counts[significant_categories + ['Other']]

    # Apply moving average for smoothing
    smoothed_counts = apply_moving_average(monthly_counts, window=smoothing_window)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each category
    for column in smoothed_counts.columns:
        ax.plot(smoothed_counts.index, smoothed_counts[column], label=column)

    # Formatting the x-axis with date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Time (6-Month Intervals)', fontsize=14)
    ax.set_ylabel('Number of Commits (Smoothed)', fontsize=14)

    # Truncate long labels for the legend
    truncated_labels = [label[:20] + '...' if len(label) > 20 else label for label in smoothed_counts.columns]

    # Add the legend with truncated labels
    ax.legend(truncated_labels, loc='upper left', bbox_to_anchor=(1, 1))  # Place legend outside the plot

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"Saved smoothed timeline chart to {save_path}")

# Define thresholds and max_labels per field
field_settings = {
    'commit_classification': {'title': 'Commit Classification Over Time', 'max_labels': 6, 'threshold': 0.02},
    'commit_complexity': {'title': 'Commit Complexity Over Time', 'max_labels': 4, 'threshold': 0.05},
    'major_related_implementation_component': {'title': 'Major Implementation Component Over Time', 'max_labels': 8, 'threshold': 0.01},
    'major_related_logic_component': {'title': 'Major Logic Component Over Time', 'max_labels': 8, 'threshold': 0.01},
}

# Generate timeline charts for categorical fields with smoothing_window=2
for field, settings in field_settings.items():
    save_path = f'imgs/timeline_{field}_smoothed.png'
    plot_frequency_timeline(
        field_name=field,
        title=settings['title'],
        max_labels=settings['max_labels'],
        threshold=settings['threshold'],
        save_path=save_path,
        smoothing_window=4  # Adjust window size as needed
    )

# Generate timeline chart for use cases or submodule events with smoothing_window=2
plot_usecases_timeline(
    title='Use Cases or Submodule Events Over Time (Smoothed)',
    save_path='imgs/timeline_usecases_or_submodule_events_smoothed.png',
    max_labels=12,
    threshold=0.005,  # Adjusted threshold for more use cases
    smoothing_window=4  # Adjust window size as needed
)

print("\nAll smoothed timeline charts have been saved successfully.")
