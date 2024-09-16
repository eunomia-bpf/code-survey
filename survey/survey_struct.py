import yaml
import json
import requests
import os
import csv
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
    prompt.append(f"  Parent Hashes: {commit_data['parent_hashes']}")
    prompt.append(f"  Refs: {commit_data['refs']}\n")
    
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
def prepare_openai_api_call(survey, commit_data):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }

    # Prepare the messages with the generated prompt and commit details
    messages = [
        {"role": "system", "content": "Answer the following survey questions based on the commit details."},
        {"role": "user", "content": generate_survey_prompt(survey, commit_data)}
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

def save_response_to_csv(content, csv_filename, commit_data):
    # Define the fieldnames (commit fields + survey response fields)
    fieldnames = list(commit_data.keys()) + list(content.keys())

    # Check if the file exists to determine if we need to write headers
    file_exists = os.path.isfile(csv_filename)

    try:
        with open(csv_filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL) 
            
            if not file_exists:
                # Write header if the file doesn't exist
                writer.writeheader()
            
            # Combine commit data with survey response content
            combined_data = {**commit_data, **content}

            # Write the row to the CSV
            writer.writerow(combined_data)
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Function to read commit data from the CSV file
def read_commit_data(commit_csv_file):
    with open(commit_csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row  # Return each commit as a dictionary
# Main function to run the process
def main(limit=3000):
    # Load the survey YAML file
    survey = load_survey("survey/commit_survey.yml")

    # Load the commit data CSV file
    commit_csv_file = "data/bpf_commits.csv"
    output_csv_file = "data/commit_survey.csv"

    # Initialize a counter
    count = 0

    # Loop through each commit data entry, limiting to the specified number
    for commit_data in read_commit_data(commit_csv_file):
        if count >= limit:
            print(f"Reached the limit of {limit} commits.")
            break
        
        print("--------------------")
        print(f"Processing Commit ID: {commit_data['commit_id']}")

        # Prepare the API call with commit data
        api_url, headers, payload = prepare_openai_api_call(survey, commit_data)

        # Send the API request and get the response
        response = send_openai_request(api_url, headers, payload)

        # Parse the content from the assistant's response
        content = json.loads(response["choices"][0]["message"]["content"])
        print(content)
        print("--------------------")

        # Save the combined commit data and response to the CSV file
        save_response_to_csv(content, output_csv_file, commit_data)

        # Increment the counter
        count += 1

    print(f"Processed {count} commits. Responses saved to '{output_csv_file}'")

if __name__ == "__main__":
    main(limit=3000)
