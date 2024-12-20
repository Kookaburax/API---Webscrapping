import json
import os

def get_model_parameters(model_name: str):
    """
    Retrieves the parameters for the specified model from the JSON configuration file.

    Args:
        model_name (str): The name of the model (e.g., "DecisionTreeClassifier").

    Returns:
        dict: A dictionary of parameters for the specified model.

    Raises:
        ValueError: If the model is not found in the configuration file.
    """
    config_path = "src/config/model_parameters.json"

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")

    with open(config_path, "r") as file:
        parameters = json.load(file)

    if model_name not in parameters:
        raise ValueError(f"Model '{model_name}' not found in the configuration file.")

    return parameters[model_name]
