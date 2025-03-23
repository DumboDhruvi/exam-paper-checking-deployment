from ocr import pdf_to_text_with_ocr
import re

def pdf_dict(pdf_path: str, api_key : str) -> dict:
    extracted_text = pdf_to_text_with_ocr(pdf_path, api_key, output_folder="output", dpi=200, delete_after_use=False)
    return raw_to_dict(extracted_text)

def raw_to_dict(extracted_text: str) -> dict:
    # Pattern to match "Question No X" with variations
    pattern = r"""(?ix)
        (?:question|questi[o0]n|qustion|questin|ques\.?)  # Variations of 'question'
        \s* no \s* (\d+)                                   # 'No' followed by number
    """
    
    # Find all question matches
    matches = list(re.finditer(pattern, extracted_text))
    
    answers = {}
    
    for i in range(len(matches)):
        # Get question number
        question_number = matches[i].group(1).strip()
        
        # Define start and end of answer text
        start = matches[i].end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(extracted_text)
        
        # Extract answer text
        answer_text = extracted_text[start:end].strip()
        
        # Pattern to remove leading "Answer" and its variations
        answer_pattern = r"^\s*(answer|anser|answ[e3]r|ans\.?|ans:|ansr|asnwer)\s*"
        
        # Remove leading "Answer" variation
        answer_text = re.sub(answer_pattern, "", answer_text, count=1, flags=re.I)
        
        # Store the cleaned answer
        answers[f"answer{question_number}"] = answer_text
    
    return answers




#testing of raw_to_dict
if __name__ == "__main__":
    text = """Question No 1 Answer This is the first answer.
    Question No 2 Answer This is the second answer.
    Question No 3 Answer This is the third answer."""

    print(raw_to_dict(text))