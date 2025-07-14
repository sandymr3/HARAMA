import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Path to your Firebase service account key
SERVICE_ACCOUNT_PATH = 'serviceAccountKey.json'

# Initialize the app
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Define your data
doc_data = {
    "exam_code": "MATH2025",
    "answer_keys": {
        "1": "Photosynthesis is the process by which ...",
        "2": "The Krebs cycle is a part of cellular respiration ...",
        "3": "Newton’s Second Law states that ..."
    },
    "created_at": datetime.utcnow(),  # Timestamp
    "created_by": "teacher_email_or_uid"
}
""""""
# Reference to the collection and document ID


def store_student_marks(student_id, exam_code, marks_dict, total_score):
    doc_id = f"{exam_code}_{student_id}"
    doc_ref = db.collection("student_marks").document(doc_id)

    doc_ref.set({
        "student_id": student_id,
        "exam_code": exam_code,
        "marks": marks_dict,
        "total_score": total_score,
        "evaluated_at": firestore.SERVER_TIMESTAMP,
        "graded_by": "system"
    })

def store_student_answers(student_id, exam_code, answers_dict):
    doc_id = f"{exam_code}_{student_id}"
    doc_ref = db.collection("student_answers").document(doc_id)

    doc_ref.set({
        "student_id": student_id,
        "exam_code": exam_code,
        "answers": answers_dict,
        "submitted_at": firestore.SERVER_TIMESTAMP,
        "source": "OCR_Gemma"
    })

def store_question_structure_flat(exam_code, question_structure, total_marks):
    doc_id = f"{exam_code}_STRUCTURE"
    doc_ref = db.collection("question_paper_structure").document(doc_id)

    doc_ref.set({
        "exam_code": exam_code,
        "max_marks": total_marks,
        "structure": question_structure,
        "created_at": firestore.SERVER_TIMESTAMP,
        "created_by": "faculty_123"
    })

# Example usage:
question_structure_flat = {
    "1ai": 5,
    "1aii": 5,
    "1b": 10,
    "2ai": 6,
    "2aii": 6,
    "2b": 8,
    "3": 20
}

store_question_structure_flat("MATH2025", question_structure_flat, total_marks=60)

