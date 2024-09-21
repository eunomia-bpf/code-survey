import csv
import yaml
import json
import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load survey from YAML file
def load_survey(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

# Generate a survey prompt based on the questions and commit data
def generate_survey_prompt(survey, commit_data):
    prompt = []
    
    # Survey information
    prompt.append(f"Survey Title: {survey['title']}\n")
    prompt.append(f"\nDescription: {survey['description']}\n")
    
    # Commit details section
    prompt.append("Commit Details:")
    prompt.append(f"  Commit ID: {commit_data['commit_id']}")
    prompt.append(f"  Author Name: {commit_data['author_name']}")
    prompt.append(f"  Author Email: {commit_data['author_email']}")
    prompt.append(f"  Commit Date: {commit_data['commit_date_timestamp']}")
    prompt.append(f"  Commit Message:\n    {commit_data['commit_message']}")
    prompt.append(f"  Changed Files: {commit_data['changed_files']}")
    prompt.append(f"  Parent Hashes: {commit_data['parent_hashes']}")
    
    # Add survey questions
    for question in survey['questions']:
        prompt.append(f"- {question['question']}\n")
    print("\n".join(prompt))
    # Return the constructed prompt as a string
    return "\n".join(prompt)


# Generate response format dynamically based on survey questions
def generate_response_format(survey):
    properties = {}
    required_fields = []

    for question in survey['questions']:
        field_name = question['id']
        field_type = question['type']
        
        if field_type == "fill_in":
            properties[field_name] = {
                "type": "string",
                "description": question['question']
            }
            required_fields.append(field_name)
        
        elif field_type == "single_choice":
            choices = [choice['value'] for choice in question['choices']]
            properties[field_name] = {
                "type": "string",
                "description": question['question'],
                "enum": choices
            }
            required_fields.append(field_name)
        
        elif field_type == "multiple_choice":
            choices = [choice['value'] for choice in question['choices']]
            properties[field_name] = {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": choices
                },
                "description": question['question']
            }
            required_fields.append(field_name)

    schema = {
        "type": "object",
        "properties": properties,
        "required": required_fields,
        "additionalProperties": False
    }

    return {
        "type": "json_schema",
        "json_schema": {
            "name": "commit_classification",
            "description": "Survey response structured for commit classification",
            "schema": schema,
            "strict": True
        }
    }

# Prepare the structured API call using the survey questions and commit data
def prepare_openai_api_call(survey, content):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }

    # Prepare the messages with the generated prompt and commit details
    messages = [
        {"role": "system", "content": "Answer the following survey questions based on the commit details."},
        {"role": "user", "content": content}
    ]

    # Generate the response format from the survey
    response_format = generate_response_format(survey)

    # Construct the payload
    payload = {
        "model": "gpt-4o-2024-08-06",
        "messages": messages,
        "response_format": response_format
    }

    return api_url, headers, json.dumps(payload)

# Send the API request
def send_openai_request(api_url, headers, payload):
    response = requests.post(api_url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed: {response.status_code} {response.text}")

# Function to save the combined commit data and response into a CSV file using pandas
def save_response_to_csv(content, csv_filename, commit_data):
    # Combine commit data with survey response content
    combined_data = {**commit_data, **content}
    
    # Convert to DataFrame
    df = pd.DataFrame([combined_data])  # [combined_data] converts dict to a one-row DataFrame
    
    # Check if file exists and write to CSV (append mode)
    if not os.path.isfile(csv_filename):
        df.to_csv(csv_filename, mode='w', index=False, quoting=csv.QUOTE_ALL)
    else:
        df.to_csv(csv_filename, mode='a', index=False, header=False, quoting=csv.QUOTE_ALL)

# Function to read commit data from the CSV file using pandas
def read_commit_data(commit_csv_file):
    # Read the CSV file into a pandas DataFrame
    return pd.read_csv(commit_csv_file)

# Function to read already processed commit IDs from the output CSV
def read_processed_commits(output_csv_file):
    if os.path.isfile(output_csv_file):
        try:
            df = pd.read_csv(output_csv_file, usecols=['commit_id'])
            return set(df['commit_id'].astype(str).tolist())
        except Exception as e:
            print(f"Error reading processed commits: {e}")
            return set()
    else:
        return set()

# Main function to run the process
def main(limit=3000):
    # Load the survey YAML file
    survey = load_survey("survey/commit_survey.yml")

    # Define file paths
    commit_csv_file = "data/bpf_commits.csv"
    output_csv_file = "data/commit_survey.csv"
    
    # Read commit data into a pandas DataFrame
    commit_df = read_commit_data(commit_csv_file)

    # Read already processed commit IDs
    processed_commits = read_processed_commits(output_csv_file)
    print(f"Found {len(processed_commits)} already processed commits.")

    # Get the total number of commits to process, excluding already processed
    commits_to_process = commit_df[~commit_df['commit_id'].astype(str).isin(processed_commits)]
    total_commits = min(len(commits_to_process), limit)
    print(f"Total commits to process: {total_commits}")

    if total_commits == 0:
        print("No new commits to process.")
        return

    # Initialize a counter
    count = 0

    # Loop through each row in the DataFrame, limiting to the specified number
    for idx, commit_data in commits_to_process.iterrows():
        if count >= limit:
            print(f"Reached the limit of {limit} commits.")
            break

        print("--------------------")
        print(f"Processing Commit {count+1}/{total_commits} - Commit ID: {commit_data['commit_id']}")

        try:
            # Prepare the API call with commit data
            prompt = generate_survey_prompt(survey, commit_data)
            api_url, headers, payload = prepare_openai_api_call(survey, prompt)

            # Send the API request and get the response
            response = send_openai_request(api_url, headers, payload)

            # Extract the content from the response
            content = json.loads(response["choices"][0]["message"]["content"])
            print("old content:")
            print(json.dumps(content, indent=2))
            rethink_times = 1
            if rethink_times > 0:
                print("Rethinking...")
                new_prompt = prompt + "\nBackground: Your previous response:\n"  + json.dumps(content, indent=2) + "Action: Do you have anything to correct? Please rethink and provide a better response. \n" + survey["hint"]
                api_url, headers, payload = prepare_openai_api_call(survey, new_prompt)
                response = send_openai_request(api_url, headers, payload)
                rethink_times -= 1
                content = json.loads(response["choices"][0]["message"]["content"])
            print("new content:")

            # Parse the content from the assistant's response
            print(json.dumps(content, indent=2))
            print("--------------------")

            # Save the combined commit data and response to the CSV file
            save_response_to_csv(content, output_csv_file, commit_data)

            # Increment the counter
            count += 1

        except Exception as e:
            print(f"Error processing commit {commit_data['commit_id']}: {e}")
            # Optionally, you can log errors to a separate file or handle them as needed

    print(f"Processed {count} commits. Responses saved to '{output_csv_file}'")

if __name__ == "__main__":
    main(limit=10000)
