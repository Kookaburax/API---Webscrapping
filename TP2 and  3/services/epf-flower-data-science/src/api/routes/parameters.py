from fastapi import HTTPException
from src.services.firestore import FirestoreClient
from fastapi import APIRouter

router = APIRouter()

@router.get("/parameters/{model_name}", tags=["Parameters"])
def get_model_parameters(model_name: str):
    """
    Retrieve parameters for a given model from Firestore.
    Args:
        model_name: Name of the model (e.g., "DecisionTreeClassifier").
    Returns:
        Parameters of the model as a JSON object.
    """
    try:
        firestore_client = FirestoreClient()
        collection_name = "parameters"

        # Retrieve the document from Firestore
        parameters = firestore_client.get(collection_name, model_name)

        return {"model_name": model_name, "parameters": parameters}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model parameters not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/parameters/{model_name}", tags=["Parameters"])
def add_model_parameters(model_name: str, parameters: dict):
    """
    Add parameters for a new model in Firestore.
    Args:
        model_name: Name of the model.
        parameters: Dictionary of parameters to store.
    Returns:
        Success message.
    """
    try:
        firestore_client = FirestoreClient()
        collection_name = "parameters"

        # Add the document to Firestore
        firestore_client.client.collection(collection_name).document(model_name).set(parameters)

        return {"message": f"Parameters for {model_name} added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/parameters/{model_name}", tags=["Parameters"])
def update_model_parameters(model_name: str, parameters: dict):
    """
    Update parameters for an existing model in Firestore.
    Args:
        model_name: Name of the model.
        parameters: Dictionary of parameters to update.
    Returns:
        Success message.
    """
    try:
        firestore_client = FirestoreClient()
        collection_name = "parameters"

        # Update the document in Firestore
        doc_ref = firestore_client.client.collection(collection_name).document(model_name)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update(parameters)
            return {"message": f"Parameters for {model_name} updated successfully."}
        else:
            raise HTTPException(status_code=404, detail=f"No parameters found for {model_name}.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")