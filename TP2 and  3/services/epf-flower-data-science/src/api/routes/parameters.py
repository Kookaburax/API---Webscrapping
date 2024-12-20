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
