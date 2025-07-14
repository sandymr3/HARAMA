import os
import google.generativeai as genai
import sys
import dotenv

dotenv.load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 500000,
    "response_mime_type": "application/json",
}
model = genai.GenerativeModel("gemma-3-27b-it", generation_config=generation_config)


def extract_answer_list(image_path: str) -> list[str]:
    try:
        image = genai.upload_file(image_path)
        model = genai.GenerativeModel("gemma-3-27b-it")
        
        prompt = """Extract the question-wise answers from the given answer sheet image. Ignore any preamble text such as headings, name, date, instructions, or introductory content. 

Return only the answer content in the following strict format as a **stringified JSON object**, like:
{
    qno1 : answer_text
    qno2 : answer_text....
}
for example:
{
  "1ai": "Data brushing allows interactive selection of data points for exploration.",
  "1b": "Linking highlights related points across multiple visualizations.",
  "2": "A confusion matrix displays predicted vs actual values in classification problems.",
  "3": "This scenario suggests a bimodal distribution based on the two visible peaks.",
  "4": "Linear regression estimates relationships between variables using best-fit lines.",
  "5": "According to the Central Limit Theorem, the sampling distribution of the mean approaches normality as sample size increases."
}

Make sure each key is a question number  and the value is the exact extracted answer text. Return only this JSON-style string without any explanation or extra formatting.
"""        
        response = model.generate_content([image, prompt])
        print(response.text)
        return response.text  # Debugging: Print response to stderr
        
    except Exception as e:
        print(f"Error in extract_answer_list: {e}", file=sys.stderr)
        return []
if __name__ == "__main__":
    
    image_path ="img1.jpg"
    answers = extract_answer_list(image_path)
    print("Extracted Answers:", answers)