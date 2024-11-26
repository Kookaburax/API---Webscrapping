from fastapi import APIRouter, HTTPException
import os
import zipfile
import subprocess
import pandas as pd

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

@router.get("/load", tags=["Data"])
def load_iris_dataset():
    """
    Loads the Iris dataset from the src/data directory as a DataFrame and returns it as JSON.
    """
    try:
        # Path to the dataset
        dataset_path = "src/data/iris.csv"

        # Check if the file exists
        if not os.path.exists(dataset_path):
            raise HTTPException(status_code=404, detail="Dataset file not found. Please download it first.")

        # Load the dataset into a Pandas DataFrame
        df = pd.read_csv(dataset_path)

        # Convert the DataFrame to JSON
        return {"data": df.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
