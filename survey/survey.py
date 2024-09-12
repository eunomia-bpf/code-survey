import csv
from typing import Optional

import yaml
from model import Choice, Items, Model, Question, Type
from pydantic import ValidationError


class Survey:
    def __init__(self):
        self.survey_model = None
        self.answers = {}

    def load_survey_config(self, file_path: str):
        """Loads the survey configuration from a YAML file."""
        try:
            with open(file_path, "r") as file:
                config_data = yaml.safe_load(file)
                self.survey_model = Model(**config_data)
                self.answers = {}
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except ValidationError as e:
            print(f"Error parsing survey config: {e}")

    def ask_question(self, question):
        """Displays the current question and handles user input, then recursively handles subquestions."""
        print(f"Question: {question.question}")

        if question.type in [Type.single_choice, Type.multiple_choice]:
            for choice in question.choices:
                print(f"- {choice.value}")

        # Ask for user input
        if question.type == Type.multiple_choice:
            answer = input(
                "Your answer (comma-separated for multiple choices): "
            ).split(",")
            answer = [ans.strip() for ans in answer]  # Clean up spaces
        else:
            answer = input("Your answer: ").strip()

        # Validate and store the answer
        self.validate_and_store_answer(question, answer)

        # If the answer leads to subquestions, recursively ask them
        if question.type in [Type.single_choice, Type.multiple_choice]:
            self.handle_subquestions(question, answer)

    def validate_and_store_answer(self, question, answer):
        """Validates the answer and stores it in the answers dictionary."""
        if question.type in [Type.single_choice, Type.multiple_choice]:
            valid_choices = [choice.value for choice in question.choices or []]

            # For multiple_choice, check each answer
            if question.type == Type.multiple_choice:
                for ans in answer:
                    if ans not in valid_choices:
                        raise ValueError(
                            f"Invalid answer: '{ans}' is not a valid option for question '{question.id}'"
                        )
            # For single_choice, validate the single answer
            elif question.type == Type.single_choice:
                if answer not in valid_choices:
                    raise ValueError(
                        f"Invalid answer: '{answer}' is not a valid option for question '{question.id}'"
                    )

        # Store the answer
        self.answers[question.id] = answer

    def handle_subquestions(self, question, answer):
        """Recursively handles subquestions based on the current answer."""
        # For multiple_choice, we need to handle each choice's subquestions
        if question.type == Type.multiple_choice:
            for ans in answer:
                for choice in question.choices:
                    if choice.value == ans and choice.subquestions:
                        for subquestion in choice.subquestions:
                            self.ask_question(subquestion)
        # For single_choice, handle the selected choice's subquestions
        elif question.type == Type.single_choice:
            for choice in question.choices:
                if choice.value == answer and choice.subquestions:
                    for subquestion in choice.subquestions:
                        self.ask_question(subquestion)

    def run_survey(self):
        """Starts the survey by asking all the main questions."""
        for question in self.survey_model.questions:
            self.ask_question(question)

    def export_answers(self) -> dict:
        """Returns all answered questions as a dictionary."""
        return self.answers

    def export_csv(self, filename: str):
        """Exports the current answers to a CSV file."""
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Question ID", "Answer"])
            for question_id, answer in self.answers.items():
                writer.writerow([question_id, answer])


# Example usage
if __name__ == "__main__":
    # File path for the survey YAML config
    config_file = "example_survey.yml"

    survey = Survey()
    survey.load_survey_config(config_file)

    if survey.survey_model:
        survey.run_survey()

        print("Survey completed.")
        print("Answers:", survey.export_answers())

        # Export answers to CSV
        survey.export_csv("survey_answers.csv")
