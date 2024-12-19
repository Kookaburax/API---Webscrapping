from fastapi import APIRouter, HTTPException
import os
import zipfile
import subprocess
import pandas as pd
import pickle

from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from src.services.parameters import get_model_parameters

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


@router.post("/process", tags=["Data"])
def process_iris_dataset():
    """
    Processes the Iris dataset by cleaning the 'species' column and normalizing features.
    """
    try:
        # Path to the dataset
        dataset_path = "src/data/iris.csv"

        # Check if the file exists
        if not os.path.exists(dataset_path):
            raise HTTPException(status_code=404, detail="Dataset file not found. Please download it first.")

        # Load the dataset into a Pandas DataFrame
        df = pd.read_csv(dataset_path)

        # Rename the columns to standardized names
        column_mapping = {
            "SepalLengthCm": "sepal_length",
            "SepalWidthCm": "sepal_width",
            "PetalLengthCm": "petal_length",
            "PetalWidthCm": "petal_width",
            "Species": "species"
        }
        df.rename(columns=column_mapping, inplace=True)

        # Remove the 'Iris-' prefix from the 'species' column
        df['species'] = df['species'].str.replace('Iris-', '', regex=False)

        # Normalize numerical features
        scaler = MinMaxScaler()
        feature_columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        df[feature_columns] = scaler.fit_transform(df[feature_columns])

        # Save the processed dataset back to a CSV file
        df.to_csv(dataset_path, index=False)

        # Return the processed dataset as JSON
        return {"processed_data": df.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



@router.post("/split", tags=["Data"])
def split_iris_dataset(test_size: float = 0.2, random_state: int = 42):
    """
    Splits the Iris dataset into training and testing sets.
    Allows specifying test size and random seed.
    """
    try:
        # Path to the dataset
        dataset_path = "src/data/iris.csv"

        # Check if the file exists
        if not os.path.exists(dataset_path):
            raise HTTPException(status_code=404, detail="Dataset file not found. Please download it first.")

        # Load the dataset into a Pandas DataFrame
        df = pd.read_csv(dataset_path)

        # Rename columns to standardized names
        column_mapping = {
            "SepalLengthCm": "sepal_length",
            "SepalWidthCm": "sepal_width",
            "PetalLengthCm": "petal_length",
            "PetalWidthCm": "petal_width",
            "Species": "species"
        }
        df.rename(columns=column_mapping, inplace=True)

        # Remove the 'Iris-' prefix from the 'species' column
        df['species'] = df['species'].str.replace('Iris-', '', regex=False)

        # Split the dataset into train and test sets
        train, test = train_test_split(
            df, test_size=test_size, random_state=random_state, stratify=df['species']
        )

        # Convert the train and test sets to JSON
        return {
            "train": train.to_dict(orient="records"),
            "test": test.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/parameters/{model_name}", tags=["Data"])
def fetch_model_parameters(model_name: str):
    """
    Fetches the model parameters for the specified model.

    Args:
        model_name (str): The name of the model (e.g., "DecisionTreeClassifier").

    Returns:
        dict: The parameters for the specified model.
    """
    try:
        parameters = get_model_parameters(model_name)
        return {"model_name": model_name, "parameters": parameters}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/train", tags=["Model"])
def train_classification_model():
    """
    Trains a Decision Tree Classifier on the processed Iris dataset
    and saves the model to the src/models directory.
    """
    try:
        # Path to the dataset
        dataset_path = "src/data/iris.csv"
        if not os.path.exists(dataset_path):
            raise HTTPException(status_code=404, detail="Processed dataset not found. Please process it first.")

        # Load the dataset
        df = pd.read_csv(dataset_path)

        # Prepare features and target
        X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
        y = df['species']

        # Train the model
        model = DecisionTreeClassifier(criterion="gini", max_depth=3)
        model.fit(X, y)

        # Save the trained model
        model_dir = "src/models"
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "iris_model.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        return {"message": "Model trained and saved successfully", "model_path": model_path}

    except Exception as e:
         raise HTTPException(status_code=500, detail=f"An error occurred during training: {str(e)}")
