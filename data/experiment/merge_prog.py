import pandas as pd

# Load your dataset
file_path = 'data/commit_survey.csv'
df = pd.read_csv(file_path)

# Define the old and new text
old_text = "A eBPF Program Logic. E.g. It affects how the kernel manages attaches or runs different types of eBPF programs such as XDP tc kprobes etc."
new_text = "eBPF events related Logic. E.g. It changes how events like XDP socket tc or tracing events like tracepoint profile k/uprobe or others like HID schedule LSM attached or affect eBPF programs."

# Replace the old text with the new text in the 'major_related_logic_component' column
df['major_related_logic_component'] = df['major_related_logic_component'].replace(old_text, new_text)

# Optionally, save the modified DataFrame to a new CSV file
output_file = 'data/commit_survey.csv'
df.to_csv(output_file)

print(f"Replaced text and saved to {output_file}")
