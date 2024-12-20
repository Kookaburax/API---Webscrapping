import os
from google.cloud import firestore

class FirestoreClient:
    """Wrapper around a Firestore database"""

    client: firestore.Client

    def __init__(self) -> None:
        """Initialize the Firestore client using the service account key."""
        # Path to the service account JSON file
        service_account_path = "src/config/service_account.json"
        if not os.path.exists(service_account_path):
            raise FileNotFoundError("Service account file not found at src/config/.")

        # Set the environment variable to point to the service account file
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path
        self.client = firestore.Client()

    def get(self, collection_name: str, document_id: str) -> dict:
        """Retrieve a document by its ID."""
        doc = self.client.collection(collection_name).document(document_id).get()
        if doc.exists:
            return doc.to_dict()
        raise FileNotFoundError(
            f"No document found in collection '{collection_name}' with ID '{document_id}'."
        )
