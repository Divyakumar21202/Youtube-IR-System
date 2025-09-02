import firebase_admin
from firebase_admin import credentials, firestore

# Global cache
_firestore_client = None

def init_firebase():
    """Initialize Firebase Admin SDK and return Firestore client."""
    global _firestore_client

    if _firestore_client is not None:
        return _firestore_client

    cred_path = "./serviceAccount.json"
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    _firestore_client = firestore.client()
    return _firestore_client

def close_firebase():
    """Close the Firebase Client & SDK"""
    _firestore_client = None

def get_firestore():
    """Get Firestore client (lazy-loaded)."""
    return init_firebase()
