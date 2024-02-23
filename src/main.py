import os

from configuration.config import JsonConfigLoader

if __name__ == '__main__':
    current_file_path = os.path.realpath(__file__)
    current_file_dir = os.path.dirname(current_file_path)

    config = JsonConfigLoader(os.path.join(current_file_dir, 'config.json'))

    print(config.get_in_dir(), config.get_out_dir())
