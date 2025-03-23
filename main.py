import json
from pdf_to_answer_dict import pdf_dict
from AnswerToMarks import Grader

def main(pdf_path: str, api_key: str, answer_key_path: str):
    """
    Extracts answers from a scanned PDF, grades them using semantic similarity, 
    and returns marks for each question.

    Args:
        pdf_path (str): Path to the scanned PDF file.
        api_key (str): API key for OCR/NLP services.
        answer_key_path (str): Path to the JSON file containing correct answers.

    Returns:
        dict: A dictionary mapping question numbers to assigned marks.
    """
    # Step 1: Extract student answers from PDF
    print("Extracting answers from PDF...")
    student_answers = pdf_dict(pdf_path, api_key)

    # Step 2: Load the answer key from a JSON file
    print("Loading correct answers...")
    with open(answer_key_path, "r", encoding="utf-8") as file:
        answer_key = json.load(file)

    # Step 3: Initialize Grader and grade answers
    print("Grading answers...")
    grader = Grader()
    scores = grader.grade_answer(student_answers, answer_key)

    # Step 4: Print and return the result
    print("Grading complete! Scores:", scores)
    return scores

# Example Usage
if __name__ == "__main__":
    pdf_file = "path/to/scanned_answers.pdf"  # Replace with actual path
    api_key = "your_api_key_here"  # If needed for OCR
    answer_key_file = "path/to/answer_key.json"  # Replace with actual path

    result = main(pdf_file, api_key, answer_key_file)
    print("Final Scores:", result)
