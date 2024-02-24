import os

from configuration.main_config_loaders import JsonConfigLoader
from configuration.input_data_loaders import JSONDataLoader
from canvas import Canvas

if __name__ == '__main__':
    current_file_path = os.path.realpath(__file__)
    current_file_dir = os.path.dirname(current_file_path)

    config = JsonConfigLoader(os.path.join(current_file_dir, 'config.json'))
    in_dir = config.get_data_dir()
    out_dir = config.get_out_dir()

    config_loader = JSONDataLoader(in_dir)

    image_height = config_loader.get_image_height()
    image_width = config_loader.get_image_width()
    figures = config_loader.get_figures()

    canvas = Canvas(image_height, image_width)
    image_draw = canvas.get_image_draw()


    for figure in figures:
        figure.draw(image_draw)

    canvas.save(out_dir)
