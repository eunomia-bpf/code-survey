import yaml
import sys
import csv
import os
from io import StringIO
from dotenv import load_dotenv
import openai
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai

def load_surveys(filename):
    with open(filename, 'r') as f:
        # Split the file content by '##' to separate multiple surveys
        content = f.read()
        surveys = [s.strip() for s in content.split('##') if s.strip()]
        parsed_surveys = []
        for survey in surveys:
            parsed_surveys.append(yaml.safe_load(survey))
        return parsed_surveys
import re

def ask_question(question, answers, buffer):
    q_text = question.get('question')
    q_type = question.get('type')
    q_id = question.get('id')
    required = question.get('required', False)
    choices = question.get('choices', [])
    subquestions = question.get('subquestions', [])

    buffer.write("\nCurrent Question:\n")
    buffer.write(f"{q_text}\n")

    def find_digit_in_response(response):
        # Look for a digit in the response and return it
        match = re.search(r'\d+', response)
        if match:
            return match.group()
        return None

    def validate_choices(ai_responses, valid_choices, num_choices):
        """ Validate if AI's responses contain at least one valid choice """
        selected_choices = []
        for resp in ai_responses:
            matched = False
            for idx, choice in enumerate(choices):
                # Match by value or index
                if resp.lower() == choice['value'].lower() or resp == str(idx + 1):
                    selected_choices.append(choice['value'])
                    matched = True
                    break
            if not matched:
                buffer.write(f"Invalid choice: '{resp}', ignoring it.\n")
        return selected_choices if len(selected_choices) >= num_choices else None

    def retry_if_invalid(prompt, valid_choices, num_choices=1):
        """ Retry mechanism if no valid input is found """
        for _ in range(3):  # Allow 3 retries
            buffer.write("Invalid or empty response, retrying...\n")
            choice_input = input_from_ai_api(prompt).strip()
            if choice_input:
                ai_responses = [resp.strip() for resp in choice_input.split(',')]
                selected_choices = validate_choices(ai_responses, valid_choices, num_choices)
                if selected_choices:
                    return selected_choices
        buffer.write("Failed to provide a valid response after 3 attempts.\n")
        return None

    if q_type == 'single_choice':
        valid_choices = [choice['value'].lower() for choice in choices]
        for idx, choice in enumerate(choices):
            buffer.write(f"{idx + 1}. {choice['value']}\n")
        prompt = buffer.getvalue()

        choice_input = input_from_ai_api(prompt).strip()
        if not choice_input:
            choice_input = retry_if_invalid(prompt, valid_choices)

        selected_choice = None
        if choice_input:
            # Try to match the AI's response with the choices
            for choice in choices:
                if choice_input.lower() == choice['value'].lower():
                    selected_choice = choice
                    break

            if not selected_choice:
                # Try matching by index (digit)
                digit = find_digit_in_response(choice_input)
                if digit and 1 <= int(digit) <= len(choices):
                    selected_choice = choices[int(digit) - 1]

        if selected_choice:
            answers[q_id] = (q_text, selected_choice['value'])
            # Handle subquestions if any
            if 'subquestions' in selected_choice:
                for subq in selected_choice['subquestions']:
                    ask_question(subq, answers, buffer)
        else:
            answers[q_id] = (q_text, choice_input)

    elif q_type == 'multiple_choice':
        valid_choices = [choice['value'].lower() for choice in choices]
        for idx, choice in enumerate(choices):
            buffer.write(f"{idx + 1}. {choice['value']}\n")
        buffer.write("You must select at least one option. You can select multiple options separated by commas. The input should only contain the numbers, without any other words.\n")
        prompt = buffer.getvalue()

        selected_choices = []
        while not selected_choices:
            choice_input = input_from_ai_api(prompt).strip()
            if choice_input:
                ai_responses = [resp.strip() for resp in choice_input.split(',')]
                selected_choices = validate_choices(ai_responses, valid_choices, 1)

            # Retry if no valid selections were made
            if not selected_choices:
                selected_choices = retry_if_invalid(prompt, valid_choices)

        answers[q_id] = (q_text, selected_choices)

    elif q_type == 'fill_in':
        prompt = buffer.getvalue()
        user_input = input_from_ai_api(prompt).strip()
        if required and not user_input:
            buffer.write("This question is required.\n")
            ask_question(question, answers, buffer)
        else:
            answers[q_id] = (q_text, user_input)

    else:
        buffer.write("Unknown question type.\n")

def run_survey(survey, data_row):
    title = survey.get('title', 'Survey')
    description = survey.get('description', '')
    questions = survey.get('questions', [])

    buffer = StringIO()
    buffer.write(f"\n{'='*50}\n{title}\n{'='*50}\n")
    buffer.write(f"{description}\n")

    # Display data row information
    buffer.write("\nInformation:\n")
    for key, value in data_row.items():
        buffer.write(f"{key}: {value}\n")

    answers = {}
    for question in questions:
        display_previous_answers(answers, buffer)
        buffer.write(f"\nSurvey Goal: {description}\n")
        ask_question(question, answers, buffer)
    # Optionally, print the buffer content for debugging
    print(buffer.getvalue())
    return answers

def display_previous_answers(answers, buffer):
    if answers:
        buffer.write("\nPrevious Questions and Answers:\n")
        for q_id, (question, answer) in answers.items():
            buffer.write(f"- {question}\n")
            if isinstance(answer, list):
                for a in answer:
                    buffer.write(f"  - {a}\n")
            else:
                buffer.write(f"  Answer: {answer}\n")

def input_from_ai_api(message: str):
    # for test:
    # print(message)
    # return input()
    # print("-" * 50)
    # print(f"Processing input: {message}")
    try:
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system",
            "content": "You are a Linux kernel maintainer. Analyze the provided information and complete the survey questions accordingly. Provide clear and concise answers."
            },
            {
            "role": "user",
            "content": f"{message}"
            }
        ],
            temperature=0.5,
            max_tokens=64,
            top_p=1
        )
        feedback = response.choices[0].message.content
        print(f"Received feedback: {feedback}")
        print("-" * 50)
        return feedback
    except Exception as e:
        print(f"Error processing input: {e}")
        exit(1)

def main(survey_file, data_file, output_file):
    # Load surveys
    surveys = load_surveys(survey_file)

    # Read data from CSV
    if not os.path.exists(data_file):
        print(f"Error: The file {data_file} does not exist.")
        sys.exit(1)

    with open(data_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_rows = list(reader)
        fieldnames = reader.fieldnames

    # Prepare to write to output CSV
    output_fieldnames = fieldnames.copy()
    # Collect all columns needed for multiple-choice options
    multiple_choice_columns = {}
    for survey in surveys:
        for question in survey.get('questions', []):
            q_id = question['id']
            if question['type'] == 'multiple_choice':
                for choice in question['choices']:
                    column_name = f"{q_id}: {choice['value']}"
                    multiple_choice_columns[column_name] = (q_id, choice['value'])
                    if column_name not in output_fieldnames:
                        output_fieldnames.append(column_name)
            elif question['type'] == 'single_choice':
                if q_id not in output_fieldnames:
                    output_fieldnames.append(q_id)
            elif question['type'] == 'fill_in':
                if q_id not in output_fieldnames:
                    output_fieldnames.append(q_id)
            # Handle subquestions
            for choice in question.get('choices', []):
                if 'subquestions' in choice:
                    for subq in choice['subquestions']:
                        subq_id = subq['id']
                        if subq['type'] == 'multiple_choice':
                            for sub_choice in subq['choices']:
                                column_name = f"{subq_id}: {sub_choice['value']}"
                                multiple_choice_columns[column_name] = (subq_id, sub_choice['value'])
                                if column_name not in output_fieldnames:
                                    output_fieldnames.append(column_name)
                        else:
                            if subq_id not in output_fieldnames:
                                output_fieldnames.append(subq_id)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile_out:
        writer = csv.DictWriter(csvfile_out, fieldnames=output_fieldnames)
        writer.writeheader()

        # Iterate over each data row
        for idx, data in enumerate(data_rows):
            print("-" * 50)
            print(f"Processing data row: {idx + 1}/{len(data_rows)}")

            # For simplicity, use the first survey
            survey = surveys[0]
            answers = run_survey(survey, data)

            # Combine data and answers
            combined_data = data.copy()
            # Initialize multiple-choice columns to 0
            for col in multiple_choice_columns.keys():
                combined_data[col] = 0

            for q_id, (_, answer) in answers.items():
                if isinstance(answer, list):
                    # For multiple-choice, set columns to 1 or 0
                    for choice_value in answer:
                        column_name = f"{q_id}: {choice_value}"
                        if column_name in combined_data:
                            combined_data[column_name] = 1
                else:
                    # For single-choice and fill-in, store the answer directly
                    combined_data[q_id] = answer

            # Write to output CSV
            writer.writerow(combined_data)

            print(f"Processed data: {data.get('id', 'N/A')}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python survey_tool.py <survey_yaml_file> <data_csv_file> <output_csv_file>")
        sys.exit(1)

    survey_file = sys.argv[1]
    data_file = sys.argv[2]
    output_file = sys.argv[3]

    main(survey_file, data_file, output_file)
