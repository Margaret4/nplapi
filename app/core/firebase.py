import firebase_admin
from firebase_admin import credentials, auth
import os

def init_firebase():
    """Initializes the Firebase Admin SDK."""
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print(f"Firebase initialized successfully using {cred_path}.")
        except Exception as e:
            print(f"Warning: Could not initialize Firebase from {cred_path}. Ensure the file exists. Error: {e}")

def verify_token(token: str):
    """Verifies a Firebase ID token and returns the decoded token."""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid or expired Firebase token: {e}")
