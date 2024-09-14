import yaml
import sys
import csv
import os

def load_surveys(filename):
    with open(filename, 'r') as f:
        # Split the file content by '##' to separate multiple surveys
        content = f.read()
        surveys = [s.strip() for s in content.split('##') if s.strip()]
        parsed_surveys = []
        for survey in surveys:
            parsed_surveys.append(yaml.safe_load(survey))
        return parsed_surveys

def display_previous_answers(answers):
    print("\nPrevious Questions and Answers:")
    for q_id, (question, answer) in answers.items():
        print(f"- {question}")
        if isinstance(answer, list):
            for a in answer:
                print(f"  - {a}")
        else:
            print(f"  Answer: {answer}")

def ask_question(question, answers):
    q_text = question.get('question')
    q_type = question.get('type')
    q_id = question.get('id')
    required = question.get('required', False)
    choices = question.get('choices', [])
    subquestions = question.get('subquestions', [])

    print("\nCurrent Question:")
    print(q_text)

    if q_type == 'single_choice':
        for idx, choice in enumerate(choices):
            print(f"{idx + 1}. {choice['value']}")
        while True:
            choice_input = input("Please select an option (enter the number): ").strip()
            if choice_input.isdigit() and 1 <= int(choice_input) <= len(choices):
                selected_choice = choices[int(choice_input) - 1]
                answers[q_id] = (q_text, selected_choice['value'])
                # Handle subquestions if any
                if 'subquestions' in selected_choice:
                    for subq in selected_choice['subquestions']:
                        ask_question(subq, answers)
                break
            else:
                print("Invalid input. Please try again.")
    elif q_type == 'multiple_choice':
        for idx, choice in enumerate(choices):
            print(f"{idx + 1}. {choice['value']}")
        print("You can select multiple options separated by commas.")
        while True:
            choice_input = input("Please select option(s): ").strip()
            indices = [i.strip() for i in choice_input.split(',')]
            if all(i.isdigit() and 1 <= int(i) <= len(choices) for i in indices):
                selected_choices = [choices[int(i) - 1]['value'] for i in indices]
                answers[q_id] = (q_text, selected_choices)
                break
            else:
                print("Invalid input. Please try again.")
    elif q_type == 'fill_in':
        while True:
            user_input = input("Your Answer: ").strip()
            if required and not user_input:
                print("This question is required.")
            else:
                answers[q_id] = (q_text, user_input)
                break
    else:
        print("Unknown question type.")

def run_survey(survey, commit_data):
    title = survey.get('title', 'Survey')
    description = survey.get('description', '')
    questions = survey.get('questions', [])

    print(f"\n{'='*50}\n{title}\n{'='*50}")
    print(description)

    # Display commit information
    print("\nInformation:")
    for key, value in commit_data.items():
        print(f"{key}: {value}")

    answers = {}
    for question in questions:
        display_previous_answers(answers)
        print(f"\nSurvey Goal: {description}")
        ask_question(question, answers)

    return answers

def main(survey_file, commits_file, output_file):
    # Load surveys
    surveys = load_surveys(survey_file)

    # Read commits from CSV
    if not os.path.exists(commits_file):
        print(f"Error: The file {commits_file} does not exist.")
        sys.exit(1)

    with open(commits_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        commits = list(reader)
        fieldnames = reader.fieldnames

    # Prepare to write to output CSV
    output_fieldnames = fieldnames.copy()
    # Add survey question IDs as fieldnames
    # Assuming all surveys have the same questions
    survey_question_ids = []
    for survey in surveys:
        for question in survey.get('questions', []):
            output_fieldnames.append(question['id'])
            # Handle subquestions
            for choice in question.get('choices', []):
                if 'subquestions' in choice:
                    for subq in choice['subquestions']:
                        output_fieldnames.append(subq['id'])

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile_out:
        writer = csv.DictWriter(csvfile_out, fieldnames=output_fieldnames)
        writer.writeheader()

        # Iterate over each commit
        for commit in commits:
            print("\n" + "#" * 80)
            print(f"Processing commit: {commit.get('commit_id')}")
            # For simplicity, use the first survey
            survey = surveys[0]
            answers = run_survey(survey, commit)

            # Combine commit data and answers
            combined_data = commit.copy()
            for q_id, (_, answer) in answers.items():
                # Flatten the answer if it's a list
                if isinstance(answer, list):
                    combined_data[q_id] = '; '.join(answer)
                else:
                    combined_data[q_id] = answer

            # Write to output CSV
            writer.writerow(combined_data)

            print("\nResponses saved.\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python survey_tool.py <survey_yaml_file> <commits_csv_file> <output_csv_file>")
        sys.exit(1)

    survey_file = sys.argv[1]
    commits_file = sys.argv[2]
    output_file = sys.argv[3]

    main(survey_file, commits_file, output_file)
