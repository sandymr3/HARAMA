from ocr_ import *
from firebase import upload_answer_key_to_firestore
import json

image_path = "img1.jpg"
ans = extract_answer_list(image_path)

# Print raw string to debug
print("Raw OCR output:")
print(repr(ans))  # helps show if it's surrounded by markdown etc.

# Clean + parse the OCR string
def parse_ocr_string_to_dict(ocr_str: str) -> dict:
    if isinstance(ocr_str, str):
        # Remove code block formatting
        raw = ocr_str.strip().replace("```json", "").replace("```", "").strip()

        # Remove triple/double quotes accidentally returned
        raw = raw.strip('"""').strip("'''").strip('"').strip("'")

        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            print("⚠️ JSON parsing failed. Trying fallback parsing...")

        # Fallback: parse manually using qno:answer style
        result = {}
        for part in raw.split(','):
            if ':' in part:
                key, value = part.split(':', 1)
                key = key.strip().strip('"').strip("'")
                value = value.strip().strip('"').strip("'")
                result[key] = value
        return result

    elif isinstance(ocr_str, dict):
        return ocr_str

    return {}

# Parse into dict
ans_dict = parse_ocr_string_to_dict(ans)

# Debug print
print("Parsed answer dict:", ans_dict)

# Upload to Firestore if valid
if ans_dict:
    upload_answer_key_to_firestore(ans_dict, "MAT2025", "email@citchennai.net")
else:
    print("❌ No valid answers parsed. Skipping upload.")
