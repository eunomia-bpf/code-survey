import yaml
import sys

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
        print("You can select multiple options separated by commas. Oly select the numbers, do not include any other words.")
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
        user_input = input("Your Answer: ").strip()
        if required and not user_input:
            print("This question is required.")
            ask_question(question, answers)
        else:
            answers[q_id] = (q_text, user_input)
    else:
        print("Unknown question type.")

def run_survey(survey):
    title = survey.get('title', 'Survey')
    description = survey.get('description', '')
    questions = survey.get('questions', [])

    print(f"\n{'='*50}\n{title}\n{'='*50}")
    print(description)

    answers = {}
    for question in questions:
        display_previous_answers(answers)
        print(f"\nSurvey Goal: {description}")
        ask_question(question, answers)

    print("\nThank you for completing the survey!")
    print("Your responses:")
    display_previous_answers(answers)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python survey_tool.py <survey_yaml_file>")
        sys.exit(1)

    filename = sys.argv[1]
    surveys = load_surveys(filename)

    for survey in surveys:
        run_survey(survey)
