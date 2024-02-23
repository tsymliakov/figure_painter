import os
import json


def merge_json_files(directory_path='data'):
    merged_data = {}

    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path, 'r') as file:
                try:
                    # Load JSON data from each file
                    json_data = json.load(file)
                    # Merge JSON data into the merged_data dictionary
                    merged_data.update(json_data)
                except Exception as e:
                    print(f"Error reading {filename}: {str(e)}")

    return merged_data


# Example usage:
merged_json = merge_json_files()
print(json.dumps(merged_json, indent=4))
