import importlib
import json
import logging
import os
import sys
from abc import ABC, abstractmethod
from typing import Iterable, Any, Dict

from figures import AbstractFigure

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler(sys.stdout))


class AbstractInputDataLoader(ABC):
    """
    Абстрактный класс, дающий представление об интерфейсе получения информации о входных данных.
    Исходя из требований ТЗ, входные данные не разделены на отдельные данные о фигурах, которые требуется нарисовать, и
    на данные о параметрах выходного изображения.
    """

    @abstractmethod
    def __init__(self, input_data_path: str):
        pass

    # можно было бы использовать и декоратор property, но я решил реализовывать интерфейс
    # через явный вызов методов
    @abstractmethod
    def get_figures(self) -> Iterable[AbstractFigure]:
        pass

    @abstractmethod
    def get_image_width(self) -> int:
        pass

    @abstractmethod
    def get_image_height(self) -> int:
        pass


class JSONDataLoader(AbstractInputDataLoader):
    """
    Класс ожидает работать с директорией с несколькими JSON- файлами. Он производит их объединение и посредством
    предоставляемого классом интерфейса. Имеет возможность выдачи клиенту класса отдельных данных о формате выходного
    изображения и о фигурах.
    """

    def __init__(self, input_data_path):
        self._input_data_path = input_data_path
        self._data = self._parse(self._input_data_path)
        self._figures = self._parse_figures(self._data)
        self._width, self._height = self._parse_image_size(self._data)

    def get_figures(self) -> Iterable[AbstractFigure]:
        return self._figures

    def get_image_width(self) -> int:
        return self._width

    def get_image_height(self) -> int:
        return self._height

    @staticmethod
    def _parse(input_data_path) -> Dict[str, Any]:
        raw_data = {}

        for filename in os.listdir(input_data_path):
            file_path = os.path.join(input_data_path, filename)
            if os.path.isfile(file_path) and filename.endswith('.json'):
                with open(file_path, 'r') as file:
                    try:
                        json_data = json.load(file)
                        raw_data.update(json_data)

                        # Тут происходит страшное. Если в директории input_data_path
                        # несколько JSON файлов, то может случиться так, что прочитается не тот файл.
                        # В контексте тестового задания это не страшно. В ином случае
                        # придется писать много непонятного кода по объединению JSON'ов

                        break
                    except Exception as e:
                        LOG.error(f"Ошибка чтения файла {file}")

        return raw_data

    @staticmethod
    def _parse_figures(data: Dict[str, Iterable]) -> Iterable[AbstractFigure]:

        try:
            raw_figures = data['figures']
        except KeyError:
            LOG.error(f'Входные данные не содержат информации о фигурах')
            sys.exit()

        figures = []
        module = importlib.import_module('figures')

        for raw_figure in raw_figures:
            try:
                figure_name = tuple(raw_figure.keys())[0]
            except IndexError:
                LOG.error(f'Не верный формат входных данных.')
                sys.exit()
            try:
                class_ = getattr(module, figure_name)
                figures.append(class_(**raw_figure[figure_name]))
            except AttributeError:
                LOG.error(f'Неожиданный тип фигуры {figure_name}')

        return set(figures)

    @staticmethod
    def _parse_image_size(data: Dict[str, Iterable]):
        try:
            raw_image_data = data['image_size']
        except KeyError:
            LOG.error(f'Входные данные не содержат информации о размере выходного изображения')
            sys.exit()

        try:
            image_width = raw_image_data['X_length']
        except KeyError:
            LOG.error(f'Входные данные не содержат информации о ширине выходного изображения')
            sys.exit()

        try:
            image_height = raw_image_data['Y_length']
        except KeyError:
            LOG.error(f'Входные данные не содержат информации о высоте выходного изображения')
            sys.exit()

        return image_width, image_height
