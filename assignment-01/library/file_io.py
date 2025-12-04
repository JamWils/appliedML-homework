import json
import os
from dataclasses import dataclass, field

@dataclass
class FStream:
    name: str
    path: str
    extension: str
    data_file: str = field(init=False)

    @classmethod
    def load_json_files(cls, path) -> dict:
        """
        Load all JSON files from the specified directory into a dictionary.
        
        Args:
            path (str): The directory path to load JSON files from.
        Returns:
            dict: A dictionary with filenames (without extension) as keys and their JSON content as values.
        """
        with open(path, "rb") as file:
            cls.data_file = json.load(file)
        
        return cls.data_file
    
    @staticmethod
    def print_json(data_file):
        """
        Print the JSON data in a formatted way.

        Args:
            data_file (dict): The JSON data to print.
        """
        print(json.dumps(data_file, indent=4, sort_keys=True))

    @classmethod
    def save_json_files(cls, path, data) -> None:
        """
        Save data to a JSON file.

        Args:
            path (str): The file path to save to.
            data (dict): The data to save.
        """
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
    