import pandas as pd
import matplotlib.pyplot as plt
import ast
import re

# Load the CSV file
file_path = 'data/commit_survey.csv'  # Update this with your actual file path
survey_data = pd.read_csv(file_path)

# Function to plot pie chart for commit classification
def plot_commit_classification_pie():
    # Get the value counts for commit classification
    value_counts = survey_data['commit_classification'].value_counts()

    # Aggregate smaller labels into "Other" if needed
    max_labels = 6
    if len(value_counts) > max_labels:
        value_counts = value_counts[:max_labels]._append(pd.Series([value_counts[max_labels:].sum()], index=['Other']))

    # Truncate labels for better readability
    truncated_labels = [label[:20] + '...' if len(label) > 10 else label for label in value_counts.index]

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(value_counts, labels=truncated_labels, autopct='%1.1f%%', startangle=90)
    # ax.set_title('Commit Classification', fontsize=12)
    
    # Save the figure
    plt.savefig('imgs/commit_pie_chart_commit_classification.png')
    plt.close()

# Function to plot pie chart for commit complexity
def plot_commit_complexity_pie():
    # Get the value counts for commit complexity
    value_counts = survey_data['commit_complexity'].value_counts()

    # Aggregate smaller labels into "Other" if needed
    max_labels = 4
    if len(value_counts) > max_labels:
        value_counts = value_counts[:max_labels]._append(pd.Series([value_counts[max_labels:].sum()], index=['Other']))

    # Truncate labels for better readability
    truncated_labels = [label[:20] + '...' if len(label) > 10 else label for label in value_counts.index]

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(value_counts, labels=truncated_labels, autopct='%1.1f%%', startangle=90)
    # ax.set_title('Commit Complexity', fontsize=12)
    
    # Save the figure
    plt.savefig('imgs/commit_pie_chart_commit_complexity.png')
    plt.close()

# Mapping long labels to short summaries
label_replacements = {
    "The implementation happens in other subsystem and is related to eBPF events. e.g. probes perf events tracepoints network scheduler HID LSM etc. Note it's still related to how eBPF programs interact with these events.": "eBPF events (tracepoints, perf, etc.)",
    "The eBPF verifier. This component ensures that eBPF programs are safe to run within the kernel.": "eBPF verifier",
    "The eBPF maps. It changes how data structures shared between user-space and kernel-space (maps) are created or managed.": "eBPF maps",
    "The eBPF JIT compiler for different architectures. It changes how eBPF bytecode is translated into machine code for different hardware architectures.": "eBPF JIT compiler",
    "The helper and kfuncs. It modifies or adds helpers and kernel functions that eBPF programs can call.": "eBPF helpers and kfuncs",
    "The syscall interface. It changes the system calls through which user-space programs interact with eBPF.": "Syscall interface"
}

# Function to plot pie chart for major implementation component
def plot_implementation_component_pie():
    # Apply the label replacements
    survey_data['major_related_implementation_component'] = survey_data['major_related_implementation_component'].replace(label_replacements)
    
    # Get the value counts for major implementation component
    value_counts = survey_data['major_related_implementation_component'].value_counts()

    # Aggregate smaller labels into "Other" if needed
    max_labels = 8
    if len(value_counts) > max_labels:
        value_counts = value_counts[:max_labels]._append(pd.Series([value_counts[max_labels:].sum()], index=['Other']))

    # Truncate labels for better readability
    truncated_labels = [label[:30] + '...' if len(label) > 10 else label for label in value_counts.index]

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(value_counts, labels=truncated_labels, autopct='%1.1f%%', startangle=90)
    
    # Save the figure
    plt.savefig('imgs/commit_pie_chart_major_implementation_component.png')
    plt.close()

# Function to plot pie chart for major logic component
def plot_logic_component_pie():
    # Get the value counts for major logic component
    value_counts = survey_data['major_related_logic_component'].value_counts()

    # Aggregate smaller labels into "Other" if needed
    max_labels = 8
    if len(value_counts) > max_labels:
        value_counts = value_counts[:max_labels]._append(pd.Series([value_counts[max_labels:].sum()], index=['Other']))

    # Truncate labels for better readability
    truncated_labels = [label[:20] + '...' if len(label) > 10 else label for label in value_counts.index]

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(value_counts, labels=truncated_labels, autopct='%1.1f%%', startangle=90)
    # ax.set_title('Major Logic Component', fontsize=12)
    
    # Save the figure
    plt.savefig('imgs/commit_pie_chart_major_logic_component.png')
    plt.close()

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

# Flatten the lists into a single series to get counts
flattened_usecases = pd.Series([usecase for sublist in survey_data['parsed_usecases'] for usecase in sublist])

# Function to plot pie chart for use cases or submodule events
def plot_usecases_or_submodule_pie():
    # Get the value counts for parsed use cases
    value_counts = flattened_usecases.value_counts()

    # Aggregate smaller labels into "Other" if needed
    max_labels = 10
    if len(value_counts) > max_labels:
        value_counts = value_counts[:max_labels]._append(pd.Series([value_counts[max_labels:].sum()], index=['Other']))

    # Truncate labels for better readability
    truncated_labels = [label[:20] + '...' if len(label) > 10 else label for label in value_counts.index]

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(value_counts, labels=truncated_labels, autopct='%1.1f%%', startangle=90)
    # ax.set_title('Use Cases or Submodule Events', fontsize=12)
    
    # Save the figure
    plt.savefig('imgs/commit_pie_chart_usecases_or_submodule_events.png')
    plt.close()

# Call the functions individually to generate and save pie charts
plot_commit_classification_pie()
plot_commit_complexity_pie()
plot_implementation_component_pie()
plot_logic_component_pie()
plot_usecases_or_submodule_pie()

print("Pie charts have been saved successfully.")
