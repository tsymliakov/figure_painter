import json
import os
from abc import ABC, abstractmethod


class AbstractFiguresLoader(ABC):
    @abstractmethod
    def __init__(self, path_to_figures_folder):
        pass

    @abstractmethod
    def get_figures(self):
        pass


class FiguresLoaderFromJson(AbstractFiguresLoader):
    """
    Класс парсит директорию с JSON-представлениями фигур и позволяет получить их в виде кортежа json- объектов.
    """

    def __init__(self, path_to_figures_folder):
        self._path_to_figures_folder = path_to_figures_folder

    def parse(self):
        merged_json_objects = []

        for filename in os.listdir(self._path_to_figures_folder):
            file_path = os.path.join(self._path_to_figures_folder, filename)
            if os.path.isfile(file_path) and filename.endswith('.json'):
                with open(file_path, 'r') as file:
                    try:
                        # Load JSON data from each file
                        json_data = json.load(file)
                        # Append JSON data to the list of merged JSON objects
                        merged_json_objects.append(json_data)
                    except Exception as e:
                        print(f"Error reading {filename}: {str(e)}")

        return tuple(merged_json_objects)

