from fastapi import APIRouter
import os
import subprocess

router = APIRouter()

@router.get("/data/download")
def download_iris_dataset():
    """
    Downloads the Iris dataset from Kaggle and saves it to the src/data directory.
    """
    try:
        # Define the Kaggle dataset identifier
        dataset = "uciml/iris"

        # Define the destination folder
        destination = "src/data"

        # Ensure the destination directory exists
        os.makedirs(destination, exist_ok=True)

        # Use the Kaggle CLI to download the dataset
        subprocess.run(["kaggle", "datasets", "download", "-d", dataset, "-p", destination], check=True)

        # Unzip the dataset (if necessary)
        for file in os.listdir(destination):
            if file.endswith(".zip"):
                subprocess.run(["unzip", "-o", os.path.join(destination, file), "-d", destination])
                os.remove(os.path.join(destination, file))

        return {"message": "Dataset downloaded successfully", "path": destination}

    except Exception as e:
        return {"error": str(e)}
