import pandas as pd
import re
import matplotlib.pyplot as plt

# Load the CSV file for analysis
file_path = 'data/commit_survey.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Filter out commits related to "bug" or "fix" in the commit classification
buggy_commits = data[data['commit_classification'].str.contains("bug|fix", case=False, na=False)]

# Exclude irrelevant components
excluded_components = [
    "The libbpf library. It affects the library that simplifies interaction with eBPF from user-space applications.",
    "The test cases and makefiles. It adds or modifies test cases or makefile scripts used for testing or building eBPF programs.",
    "It's not related to any above. It affects an implementation component not listed but does related to the BPF subsystem.",
    "It's not related to any above. It affects an implementation component is totally unrelated to the BPF subsystem.",
    "The bpftool utility. It modifies the bpftool utility used for introspecting and interacting with eBPF programs and maps."
]

# Filter the dataset for relevant buggy components
filtered_buggy_components = buggy_commits[~buggy_commits['major_related_implementation_component'].isin(excluded_components)]

# Drop entries that are unrelated
filtered_buggy_components_cleaned = filtered_buggy_components[~filtered_buggy_components['major_related_implementation_component'].str.contains("not related", case=False, na=False)]

# Mapping long labels to short summaries
label_replacements = {
    "The implementation happens in other subsystem and is related to eBPF events. e.g. probes perf events tracepoints network scheduler HID LSM etc. Note it's still related to how eBPF programs interact with these events.": "eBPF events (tracepoints, perf, etc.)",
    "The eBPF verifier. This component ensures that eBPF programs are safe to run within the kernel.": "eBPF verifier",
    "The eBPF maps. It changes how data structures shared between user-space and kernel-space (maps) are created or managed.": "eBPF maps",
    "The eBPF JIT compiler for different architectures. It changes how eBPF bytecode is translated into machine code for different hardware architectures.": "eBPF JIT compiler",
    "The helper and kfuncs. It modifies or adds helpers and kernel functions that eBPF programs can call.": "eBPF helpers and kfuncs",
    "The syscall interface. It changes the system calls through which user-space programs interact with eBPF.": "Syscall interface"
}

# Apply these replacements to the component column
filtered_buggy_components_cleaned['short_component'] = filtered_buggy_components_cleaned['major_related_implementation_component'].replace(label_replacements)

# Group other components under 'Others'
main_components = ["eBPF events (tracepoints, perf, etc.)", "eBPF verifier", "eBPF maps", "eBPF JIT compiler", "eBPF helpers and kfuncs", "Syscall interface"]
filtered_buggy_components_cleaned['short_component'] = filtered_buggy_components_cleaned['short_component'].apply(lambda x: x if x in main_components else "Others")

# Count the number of bugs per component
component_bug_counts = filtered_buggy_components_cleaned['short_component'].value_counts()

# Extract file paths and count the occurrences
def extract_valid_file_paths(changed_files_entry):
    file_paths = re.findall(r'([a-zA-Z0-9_/.-]+\.[ch])', changed_files_entry)
    return file_paths if file_paths else []

all_valid_changed_files = filtered_buggy_components_cleaned['changed_files'].dropna().apply(extract_valid_file_paths).explode()

# Top 10 files with the most bug fixes
top_valid_buggy_files = all_valid_changed_files.value_counts().head(10)

# Save the pie chart of kernel components with most bugs to a variable
fig, ax = plt.subplots(figsize=(10, 6))
component_bug_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, ax=ax)
# plt.title('Kernel Implementation Components with the Most Bugs')
plt.ylabel('')
plt.tight_layout()

# Save the figure to a variable
v = fig

# Print the top 10 most buggy files
print("Top 10 Files with the Most Bug Fixes:\n", top_valid_buggy_files)

# # Show the pie chart (saved in variable 'v')
plt.savefig('imgs/kernel_components_most_buggy_pie_chart.pdf')
