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

def upload_answer_key_to_firestore(answer_dict, exam_code, teacher_email):
    doc_ref = db.collection("answer_keys").document(exam_code)
    
    doc_data = {
        "exam_code": exam_code,
        "answer_keys": answer_dict,
        "created_by": teacher_email,
        "created_at": firestore.SERVER_TIMESTAMP
    }

    doc_ref.set(doc_data)
    print(f"Answer key uploaded for exam {exam_code}")
