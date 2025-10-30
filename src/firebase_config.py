import firebase_admin
from firebase_admin import credentials, firestore, auth

if not firebase_admin._apps:

    cred = credentials.Certificate("H:/Projects/mchatbot/src/firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
