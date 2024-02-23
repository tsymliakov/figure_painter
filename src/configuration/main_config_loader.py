import sys
from abc import ABC, abstractmethod
import json
import logging

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler(sys.stdout))


class AbstractConfigLoader(ABC):
    """
    Абстрактный класс, представляющий собой интерфейс, посредством которого программа получает конфигуарционный файл,
    содержащий в себе информацию о входной и выходной директориях.

    Входная директория содержит файл, задающий параметры фигур, которые требуется нарисовать.
    Выходная директория служит для сохранения итогового изображения.
    """

    def __init__(self, config_path):
        self._config_path = config_path
        self._parse_config()

    @abstractmethod
    def _parse_config(self):
        self._data_root_folder = ''
        self._output_folder = ''

    def get_in_dir(self):
        return self._data_root_folder

    def get_out_dir(self):
        return self._output_folder


class JsonConfigLoader(AbstractConfigLoader):
    def _parse_config(self):
        try:
            with open(self._config_path) as config:
                jsn_config = json.load(config)
                data_root_folder = jsn_config.get("data_root_folder")

                if data_root_folder is None:
                    LOG.error('Конфигурационный файл не содержит информации о входной директории.')

                output_folder = jsn_config.get("output_folder")

                if output_folder is None:
                    LOG.error('Конфигурационный файл не содержит информации о выходной директории.')

                self._data_root_folder = data_root_folder
                self._output_folder = output_folder

        except FileNotFoundError:
            LOG.error(f'Конфигурационный файл "{self._config_path}" не найден.')
            sys.exit(1)
        except PermissionError:
            LOG.error(f'Нет достаточных прав для чтение конфигурационного файла "{self._config_path}".')
            sys.exit(1)
