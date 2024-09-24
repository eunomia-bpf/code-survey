import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
file_path = 'data/commit_survey.csv'   # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Keywords to filter commits
keywords = ['bpf_link', 'dynptr', 'token', 'bpf_iter', 'tail_call', 'bpf_timer', 'spin_lock']

# Filter out rows where the implementation component contains test cases or is marked as unrelated/not sure
filtered_df = df[~df['major_related_implementation_component'].str.contains('test', case=False, na=False) &
                 ~df['major_related_implementation_component'].str.contains('not related', case=False, na=False) &
                 ~df['major_related_implementation_component'].str.contains('not sure', case=False, na=False)]

# Create an empty DataFrame to store the counts of each keyword for each implementation component
keyword_component_counts = pd.DataFrame()

# Iterate through each keyword to calculate the counts of related implementation components
for keyword in keywords:
    keyword_commits = filtered_df[filtered_df['commit_message'].str.contains(keyword, case=False, na=False) | 
                                  filtered_df['summary'].str.contains(keyword, case=False, na=False)]
    
    keyword_implementation_component = keyword_commits[['major_related_implementation_component', 'commit_id']]
    component_count = keyword_implementation_component.groupby('major_related_implementation_component').count()
    component_count.columns = [keyword]
    
    # Merge with the main DataFrame to accumulate the counts
    if keyword_component_counts.empty:
        keyword_component_counts = component_count
    else:
        keyword_component_counts = keyword_component_counts.merge(component_count, left_index=True, right_index=True, how='outer')

# Fill any missing values with 0
keyword_component_counts.fillna(0, inplace=True)

# Limit the label length to a maximum of 20 characters for readability
keyword_component_counts.index = keyword_component_counts.index.str[:20]

# Create the heatmap
plt.figure(figsize=(8, 5))
sns.heatmap(keyword_component_counts, annot=True, fmt="g", cmap='Blues', cbar=True)
# plt.title("Heatmap of BPF Link, Dynptr, Token, BPF Iter, Tail Call, BPF Timer, and Spin Lock Commits vs. Implementation Components")
plt.ylabel("Implementation Component")
plt.xlabel("Keywords")
plt.tight_layout()
plt.savefig('imgs/heatmap_bpf_keywords_vs_components.png')
