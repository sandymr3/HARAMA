import os
import google.generativeai as genai
import sys
import dotenv

dotenv.load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def run_gemini_ocr(image_path: str) -> str:
    try:
        image = genai.upload_file(image_path)
        model = genai.GenerativeModel("gemma-3-27b-it")
        response = model.generate_content([image, "Extract text from the image and just return the contents of the image."])
        return response.text
    except Exception as e:
        return ""

def extract_answer_list(image_path: str) -> list[str]:
    try:
        image = genai.upload_file(image_path)
        model = genai.GenerativeModel("gemma-3-27b-it")
        
        prompt = """extract the text from the following answersheet and just return in the format of [1:(textcontent) ,2:.....,3:......] like that no headers or footers."""
        
        response = model.generate_content([image, prompt])
        
        # Extract the list from the response
        response_text = response.text.strip()
        
        return response_text  # Debugging: Print response to stderr
        
    except Exception as e:
        return []

if __name__ == "__main__":
    image_path = "img2.jpg"  # Replace with your actual image path
    answer_list = extract_answer_list(image_path)
    print(answer_list)