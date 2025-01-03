import json
import os

class JSONManager:
    def create_json(self, data, json_file):
        """
        Create a new JSON file with the standardized structure.
        :param data: A dictionary containing 'title', 'headers', and 'rows'.
        :param json_file: The path of the JSON file to create.
        """
        if not all(key in data for key in ["title", "headers", "rows"]):
            raise ValueError("Data must contain 'title', 'headers', and 'rows'.")

        # Write the data to the JSON file
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

    def append_to_json(self, new_row, json_file):
        """
        Append a new row to an existing JSON file.
        :param new_row: A list representing a new row of data.
        :param json_file: The path of the JSON file to append to.
        """
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"JSON file '{json_file}' not found.")

        with open(json_file, "r") as f:
            data = json.load(f)

        if "rows" not in data:
            raise ValueError("JSON file must contain a 'rows' key.")

        # Append the new row
        data["rows"].append(new_row)

        # Write back to the JSON file
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

    def read_json(self, json_file):
        """
        Read and validate a JSON file.
        :param json_file: The path of the JSON file to read.
        :return: The parsed JSON data.
        """
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"JSON file '{json_file}' not found.")

        with open(json_file, "r") as f:
            data = json.load(f)

        if not all(key in data for key in ["title", "headers", "rows"]):
            raise ValueError("JSON file must contain 'title', 'headers', and 'rows'.")

        return data