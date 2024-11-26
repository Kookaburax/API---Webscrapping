from fastapi import APIRouter
import os
import zipfile
import subprocess

router = APIRouter()  # Define the APIRouter instance

@router.get("/download", tags=["Data"])
def download_iris_dataset():
    """
    Downloads the Iris dataset from Kaggle and saves it to the src/data directory.
    """
    try:
        dataset = "uciml/iris"
        destination = "src/data"
        os.makedirs(destination, exist_ok=True)

        # Download dataset
        subprocess.run(["kaggle", "datasets", "download", "-d", dataset, "-p", destination], check=True)

        # Unzip dataset if needed
        for file in os.listdir(destination):
            if file.endswith(".zip"):
                with zipfile.ZipFile(os.path.join(destination, file), 'r') as zip_ref:
                    zip_ref.extractall(destination)
                os.remove(os.path.join(destination, file))  # Clean up zip file

        return {"message": "Dataset downloaded successfully", "path": destination}

    except Exception as e:
        return {"error": str(e)}
