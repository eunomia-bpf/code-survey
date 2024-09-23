import pandas as pd
import  ast
import re

# Load the CSV file (you can replace the path with your local path)
file_path = 'data/commit_survey.csv'
df = pd.read_csv(file_path)

# total numer
total_commits = df.shape[0]
print(f"Total number of commits: {total_commits}")

# 1. Distribution of all the fields related to the survey
print("Analyzing the distribution of all fields related to the survey to understand the overall commit characteristics and identify potential areas of focus or concern.")

# Commit classification distribution
commit_classification_distribution = df['commit_classification'].value_counts()
print("\nBy analyzing the commit classification distribution, we can identify the types of changes most frequently made. This helps in understanding the development priorities and ensuring that the commit classifications are consistent.")

# Commit complexity distribution
commit_complexity_distribution = df['commit_complexity'].value_counts()
print("\nAnalyzing the commit complexity distribution helps us understand the typical scope of changes being made. This is important for assessing the risk associated with commits and ensuring that the complexity levels are consistently categorized.")

# Major related implementation component distribution
implementation_component_distribution = df['major_related_implementation_component'].value_counts()
print("\nEvaluating the major related implementation component distribution allows us to see which parts of the codebase are most affected by changes. This can highlight hotspots and help in allocating resources for code reviews or testing.")

# Major related logic component distribution
logic_component_distribution = df['major_related_logic_component'].value_counts()
print("\nAssessing the major related logic component distribution provides insights into which logical areas are undergoing the most changes. This is crucial for understanding the impact on system functionality and maintaining code integrity.")

# Displaying the results
print("\n1. Distribution of all fields related to the survey:\n")
print("Commit Classification Distribution:\n", commit_classification_distribution)
print("\nCommit Complexity Distribution:\n", commit_complexity_distribution)
print("\nMajor Related Implementation Component Distribution:\n", implementation_component_distribution)
print("\nMajor Related Logic Component Distribution:\n", logic_component_distribution)

# 2. Distribution of other fields when the commit is classified as a merge commit
print("\n\n2. Analyzing distribution of other fields when the commit is classified as a merge commit to check for consistency in classification and to ensure merges are appropriately handled.")

# Filter the dataset to include only rows where the commit classification is "merge commit"
merge_classification_df = df[df['commit_classification'].str.contains("merge commit", case=False, na=False)]

# Merge commit complexity distribution
merge_commit_complexity_distribution = merge_classification_df['commit_complexity'].value_counts()
print("\nAnalyzing the complexity distribution of merge commits helps verify that they are correctly identified as 'Merge-like' in complexity, ensuring consistency in how we categorize these commits.")

# Merge commit implementation component distribution
merge_commit_implementation_distribution = merge_classification_df['major_related_implementation_component'].value_counts()
print("\nExamining the implementation components affected by merge commits allows us to see if merges are correctly impacting multiple components, as expected. This helps maintain the accuracy of our component classifications.")

# Merge commit logic component distribution
merge_commit_logic_distribution = merge_classification_df['major_related_logic_component'].value_counts()
print("\nSimilarly, analyzing the logic components for merge commits helps us ensure that the logical areas affected by merges are appropriately categorized.")

# Displaying the results
print("\nMerge Commit Complexity Distribution:\n", merge_commit_complexity_distribution)
print("\nMerge Commit Implementation Component Distribution:\n", merge_commit_implementation_distribution)
print("\nMerge Commit Logic Component Distribution:\n", merge_commit_logic_distribution)

# 3. Distribution of eBPF events related Logic and Other Subsystem Implementation related to eBPF events
print("\n\n3. Analyzing the distribution of eBPF Events Related Logic and Implementation in Other Subsystems to understand the integration points and ensure consistency in event-related classifications.")

# Distribution of eBPF events related Logic
ebpf_events_related_logic_df = df[df['major_related_logic_component'].str.contains('eBPF events related Logic', case=False, na=False)]
ebpf_events_related_logic_distribution = ebpf_events_related_logic_df['major_related_logic_component'].value_counts()
print("\nBy analyzing eBPF events related logic, we can gauge the focus on event handling within eBPF, ensuring that event-related changes are correctly classified and consistently tracked.")

# Distribution of implementation in other subsystems related to eBPF events
other_subsystems_related_implementation_df = df[df['major_related_implementation_component'].str.contains('related to eBPF events', case=False, na=False)]
other_subsystems_related_implementation_distribution = other_subsystems_related_implementation_df['major_related_implementation_component'].value_counts()
print("\nAssessing the implementation in other subsystems related to eBPF events helps us understand cross-component interactions and ensures that such implementations are accurately captured for consistency.")

print("\nDistribution of eBPF Events Related Logic:\n", ebpf_events_related_logic_distribution)
print("\nDistribution of Implementation in Other Subsystems Related to eBPF Events:\n", other_subsystems_related_implementation_distribution)

# Additional analysis with 'usecases_or_submodule_events'
print("\nWe will now delve deeper by analyzing the 'usecases_or_submodule_events' field to understand the specific use cases or events that commits relate to. This analysis helps in verifying consistency between the use cases/events and the related logic or implementation components.")
print("Note if one meaningful use case is present, it is enough to classify the commit.")
print("so we will check if there are multiple use cases, we will remove 'It's not related to any above' if other valid use cases exist.")
print("since this is a muplti-choice field, we will parse the string representation of lists to accurately count the occurrences of each use case or event.")
# The 'usecases_or_submodule_events' field may contain multiple choices per commit, stored as strings representing lists.
# We need to parse these strings into actual lists for accurate analysis.

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
df['parsed_usecases'] = df['usecases_or_submodule_events'].apply(parse_usecases)

# Explaining the importance of parsing
print("\nBy parsing the 'usecases_or_submodule_events' field, we can accurately count the occurrences of each use case or event, which is essential for understanding the distribution and ensuring consistency in classifications.")

# Flatten the list of use cases into a single list to count occurrences
usecase_list = [usecase for sublist in df['parsed_usecases'] for usecase in sublist]

# Create a DataFrame to count the occurrences of each use case
usecase_counts = pd.Series(usecase_list).value_counts()

print("\nDistribution of Use Cases or Submodule Events:")
print(usecase_counts)

# Cross-analysis: Compare use cases with eBPF events related logic
print("\nCross-analyzing the use cases with the 'eBPF events related Logic' commits to check for consistency in data labeling.")

# Filter commits that are both in 'eBPF events related Logic' and have specific use cases
ebpf_events_with_usecases = ebpf_events_related_logic_df.copy()
ebpf_events_with_usecases['parsed_usecases'] = ebpf_events_with_usecases['usecases_or_submodule_events'].apply(parse_usecases)

# Count use cases within eBPF events related logic
usecase_list_ebpf_events = [usecase for sublist in ebpf_events_with_usecases['parsed_usecases'] for usecase in sublist]
usecase_counts_ebpf_events = pd.Series(usecase_list_ebpf_events).value_counts()

print("\nUse Cases within eBPF Events Related Logic:")
print(usecase_counts_ebpf_events)

# Analyzing consistency by checking if use cases align with the logic component
print("\nThis analysis helps us determine whether the use cases specified in the commits align with their classification as 'eBPF events related Logic', ensuring consistency and correctness in data labeling.")

# Further Cross-analysis: Compare use cases with Implementation in Other Subsystems
print("\nSimilarly, cross-analyzing the use cases with commits involving Implementation in Other Subsystems related to eBPF events.")

other_subsystems_with_usecases = other_subsystems_related_implementation_df.copy()
other_subsystems_with_usecases['parsed_usecases'] = other_subsystems_with_usecases['usecases_or_submodule_events'].apply(parse_usecases)

# Count use cases within other subsystems related implementation
usecase_list_other_subsystems = [usecase for sublist in other_subsystems_with_usecases['parsed_usecases'] for usecase in sublist]
usecase_counts_other_subsystems = pd.Series(usecase_list_other_subsystems).value_counts()

print("\nUse Cases within Implementation in Other Subsystems Related to eBPF Events:")
print(usecase_counts_other_subsystems)

print("\nBy comparing these distributions, we can identify any discrepancies in data labeling and ensure that the commits are consistently classified across different fields, enhancing data correctness and reliability.")

# Check for commits where use cases do not match the expected logic component
print("\nIdentifying any inconsistencies where commits classified as 'eBPF events related Logic' do not have corresponding event-related use cases.")

# For 'eBPF events related Logic', find commits with no event-related use cases
event_related_usecases = [
    "XDP related type programs. It relates to programs handling high-performance packet processing through the XDP framework.",
    "Socket related type programs. It relates to programs that process socket-level events such as filtering or manipulating socket traffic.",
    "tc related type programs. It affects programs managing traffic control (tc) for queuing or prioritizing network traffic.",
    "Netfilter related type programs. It impacts programs interacting with the Netfilter framework used in packet filtering and NAT.",
    "Tracepoints related type programs. It modifies programs that attach to tracepoints for low-level kernel event tracing.",
    "kprobe/ftrace like type kernel dynamic probe programs. It affects kernel-level probes used for tracing kernel functions. It can be other kernel probes in perf-events.",
    "uprobe/usdt like type user-space dynamic probe programs. It impacts user-space probes for tracing user-space applications. It can be other user-space probes in perf-events.",
    "Profile related type programs. It affects programs used for profiling system or application performance.",
    "LSM type related programs. It relates to eBPF programs used with Linux Security Modules (LSMs) for security enhancements.",
    "Struct_ops type related programs. It affects programs tha t allows user-defined methods to be called by subsystems.",
    "cgroup type related programs. It affects programs managing resource limits or network behavior via control groups (cgroups).",
    "HID driver related type programs. It relates to programs interacting with HID (Human Interface Devices) for input/output events.",
    "Scheduler related type programs. It modifies programs that interact with kernel-level scheduling mechanisms."
]

# Function to check if any use case in the list matches event-related use cases
def has_event_related_usecase(usecase_list):
    return any(usecase in event_related_usecases for usecase in usecase_list)

# Filter commits where event-related logic does not have event-related use cases
inconsistencies = ebpf_events_with_usecases[~ebpf_events_with_usecases['parsed_usecases'].apply(has_event_related_usecase)]

print(f"\nNumber of commits with 'eBPF events related Logic' but without corresponding event-related use cases: {inconsistencies.shape[0]}")

# Sample commit messages of inconsistencies
if inconsistencies.shape[0] > 0:
    print("\nSample commit messages of inconsistent commits:")
    print(inconsistencies['commit_message'].head(5))
else:
    print("\nNo inconsistencies found. All commits with 'eBPF events related Logic' have corresponding event-related use cases.")

print("\nThis check helps in verifying the consistency of data labeling, ensuring that the logical components and use cases are aligned. Identifying and correcting any inconsistencies enhances the overall correctness of the dataset.")

# 4. Not related to the BPF subsystem analysis
print("\n\n4. Identifying commits marked as 'Not related to BPF subsystem' to assess data correctness and determine if any irrelevant commits are affecting our analysis.")

# Filter the dataset to find commits marked as "Not related to BPF subsystem" in both implementation and logic fields
not_related_implementation = df[df['major_related_implementation_component'].str.contains("not related", case=False, na=False)]
not_related_logic = df[df['major_related_logic_component'].str.contains("not related", case=False, na=False)]

# Check commit messages for further investigation (print a sample)
print("\nSample Commit Messages of 'Not related to BPF subsystem' in Implementation Component:")
not_related_implementation_commit_messages = not_related_implementation['commit_message'].head(10)
print(not_related_implementation_commit_messages)

print("\nSample Commit Messages of 'Not related to BPF subsystem' in Logic Component:")
not_related_logic_commit_messages = not_related_logic['commit_message'].head(10)
print(not_related_logic_commit_messages)

# 5. Find commits classified as merge but not merge in implementation or logic components
print("\n\n5. Checking for consistency by finding commits classified as merge but not marked as merge in Implementation or Logic components. This helps in identifying any discrepancies in commit classification.")

# Find cases where commit is classified as merge but implementation or logic is not merge
merge_classification_implementation_mismatch = merge_classification_df[~merge_classification_df['major_related_implementation_component'].str.contains("merge commit", case=False, na=False)]
merge_classification_logic_mismatch = merge_classification_df[~merge_classification_df['major_related_logic_component'].str.contains("merge commit", case=False, na=False)]

# Calculate the percentage of mismatches
total_commits = df.shape[0]
total_merge_commits = merge_classification_df.shape[0]
implementation_mismatches = merge_classification_implementation_mismatch.shape[0]
logic_mismatches = merge_classification_logic_mismatch.shape[0]

implementation_mismatch_percentage = (implementation_mismatches / total_merge_commits) * 100
logic_mismatch_percentage = (logic_mismatches / total_merge_commits) * 100

# Output the mismatched results
print(f"\nNumber of mismatches in implementation: {implementation_mismatches} ({implementation_mismatch_percentage:.2f}% of merge commits)")
print(f"Number of mismatches in logic: {logic_mismatches} ({logic_mismatch_percentage:.2f}% of merge commits)")
print("\nAnalyzing these mismatches helps ensure that merges are consistently classified across different fields, which is essential for data correctness and consistency.")

print("\nTop 10 Commit Messages (Merge in Classification but not in Implementation):")
merge_implementation_mismatch_commit_messages = merge_classification_implementation_mismatch['commit_message'].head(10)
print(merge_implementation_mismatch_commit_messages)

print("\nTop 10 Commit Messages (Merge in Classification but not in Logic):")
merge_logic_mismatch_commit_messages = merge_classification_logic_mismatch['commit_message'].head(10)
print(merge_logic_mismatch_commit_messages)

# 6. Mismatch Analysis
print("\n\n6. Mismatch Analysis:")
print(f"Total number of commits: {total_commits}")
print(f"Total number of merge commits: {total_merge_commits}")
print(f"Number of mismatches in implementation: {implementation_mismatches} ({implementation_mismatch_percentage:.2f}% of merge commits)")
print(f"Number of mismatches in logic: {logic_mismatches} ({logic_mismatch_percentage:.2f}% of merge commits)")
print("\nThis analysis helps in quantifying the extent of inconsistencies in the data, which is crucial for improving data quality and ensuring accurate analyses.")

# 7. 'Not related to BPF subsystem' Analysis
print("\n\n7. 'Not related to BPF subsystem' Analysis:")
print("Calculating the number of commits marked as 'Not related to BPF subsystem' to evaluate the presence of irrelevant data that may affect the correctness of our analysis.")

# Calculate percentage of commits marked as "Not related to BPF subsystem"
not_related_implementation_count = not_related_implementation.shape[0]
not_related_logic_count = not_related_logic.shape[0]

not_related_implementation_percentage = (not_related_implementation_count / total_commits) * 100
not_related_logic_percentage = (not_related_logic_count / total_commits) * 100

# # Output the percentage of commits marked as "Not related to BPF subsystem"
# print(f"Number of commits marked as 'Not related to BPF subsystem' in Implementation Component: {not_related_implementation_count} ({not_related_implementation_percentage:.2f}% of total commits)")
# print(f"Number of commits marked as 'Not related to BPF subsystem' in Logic Component: {not_related_logic_count} ({not_related_logic_percentage:.2f}% of total commits)")

# # Check if there's any significant mismatch in these percentages
# if not_related_implementation_percentage > 5 or not_related_logic_percentage > 5:
#     print("\nThere is a significant number of commits marked as 'Not related to BPF subsystem'. This indicates potential data quality issues and suggests that data cleaning may be necessary to improve analysis correctness.")
# else:
#     print("\nThe number of commits marked as 'Not related to BPF subsystem' is relatively low and does not significantly affect overall analysis correctness.")

print("\nSample Commit Messages of 'Not related to BPF subsystem' in Implementation Component:")
print(not_related_implementation_commit_messages)

print("\nSample Commit Messages of 'Not related to BPF subsystem' in Logic Component:")
print(not_related_logic_commit_messages)
