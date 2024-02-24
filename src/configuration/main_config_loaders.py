import sys
from abc import ABC, abstractmethod
import json
import logging

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler(sys.stdout))


INPUT_DATA_DIR = 'data_root_folder'
OUTPUT_DIR = 'output_folder'


class AbstractConfigLoader(ABC):
    """
    Абстрактный класс, представляющий собой интерфейс, посредством которого программа получает конфигуарционный файл,
    содержащий в себе информацию о входной и выходной директориях.

    Входная директория содержит файл, задающий параметры фигур, которые требуется нарисовать.
    Выходная директория служит для сохранения итогового изображения.
    """

    def __init__(self, config_path):
        self._input_data_folder, self._output_folder = self._parse_config(config_path)

    @abstractmethod
    def _parse_config(self, config_path):
        pass

    def get_data_dir(self):
        return self._input_data_folder

    def get_out_dir(self):
        return self._output_folder


class JsonConfigLoader(AbstractConfigLoader):
    def _parse_config(self, config_path):
        try:
            with open(config_path) as config:
                jsn_config = json.load(config)
                input_data_folder = jsn_config.get(INPUT_DATA_DIR)

                if input_data_folder is None:
                    LOG.error('Конфигурационный файл не содержит информации о входной директории.')
                    sys.exit()

                output_folder = jsn_config.get(OUTPUT_DIR)

                if output_folder is None:
                    LOG.error('Конфигурационный файл не содержит информации о выходной директории.')
                    sys.exit()

                return input_data_folder, output_folder

        except FileNotFoundError:
            LOG.error(f'Конфигурационный файл "{config_path}" не найден.')
            sys.exit()
        except PermissionError:
            LOG.error(f'Нет достаточных прав для чтение конфигурационного файла "{config_path}".')
            sys.exit()
