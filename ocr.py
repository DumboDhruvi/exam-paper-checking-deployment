from pdf2image import convert_from_path
import requests
import os

def pdf_to_text_with_ocr(pdf_path, api_key, output_folder="output", dpi=200, delete_after_use=False):
    """
    Converts a PDF to images, checks file size, performs OCR, and deletes unused images.
    
    Parameters:
    - pdf_path (str): Path to the PDF file.
    - api_key (str): API key for OCR.Space.
    - output_folder (str): Folder for temporary images.
    - dpi (int): Resolution of images (default: 150).
    - delete_after_use (bool): Whether to delete images after OCR.
    
    Returns:
    - Extracted text from the PDF or exits if file size is too large.
    """
    os.makedirs(output_folder, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=dpi)
    extracted_text = ""
    image_paths = []

    for i, img in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i+1}.jpg")
        img.save(image_path, "JPEG", quality=95)  # Save with high quality
        image_paths.append(image_path)

        # Check file size
        file_size = os.path.getsize(image_path)
        if file_size > 1024 * 1024:  # 1MB
            print(f"Image {image_path} is too large ({file_size / 1024:.2f} KB). Please reduce size manually using dpi parameter.")
            return  # Exit the function

        # Perform OCR
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                "https://api.ocr.space/parse/image",
                files={"image": image_file},
                data={"apikey": api_key, "OCREngine": 2, "isTable": True},
            )

        result = response.json()
        print(f"API Response recived for page {i}")  # Debugging step

        if "ParsedResults" in result:
            extracted_text += f"page{i}: " + result["ParsedResults"][0]["ParsedText"] + "\n"
        else:
            print(f"Error: 'ParsedResults' missing. Full response: psge mo:{i}")
            extracted_text += f"\n[Error: OCR failed for this page {i}]\n"

    # Delete images after OCR only warning comment out if needed
    if delete_after_use:
        for img_path in image_paths:
            os.remove(img_path)
        print("Temporary images deleted.")

    return extracted_text

# Example usage
if __name__ == "__main__":
    pdf_file = r""  # Replace with your PDF file
    api_key = ""  # Replace with your actual API key of easyocr or other api

    text = pdf_to_text_with_ocr(pdf_file, api_key)
    print("Extracted Text:\n", text)

