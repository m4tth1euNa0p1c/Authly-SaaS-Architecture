import os
import firebase_admin
from firebase_admin import credentials, auth
from app.config.settings import settings

def init_firebase():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, settings.firebase_service_account_path)
    print("Initializing Firebase with service account file at:", SERVICE_ACCOUNT_PATH)
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully.")
        except Exception as e:
            print("Error initializing Firebase:", e)
            raise e

init_firebase()

def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise e
