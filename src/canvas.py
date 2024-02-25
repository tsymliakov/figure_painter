import logging
import os
import sys

from PIL import Image, ImageDraw, ImageOps

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler(sys.stdout))


class Canvas:
    def __init__(self, width: int, height: int):
        self._img = Image.new("RGB", (width, height), "white")

    def get_image_draw(self):
        return ImageDraw.Draw(self._img)

    def save(self, path, format_='PNG'):
        if not os.path.isdir(path):
            os.makedirs(path)

        try:
            image_path = os.path.join(os.path.abspath(path), f'image.{format_.lower()}')

            # Я прямо-таки горжусь этим хаком. Координатная сетка в pillow имеет координаты (0, 0)
            # в левом верхнем углу, а не в человеческом левом нижнем
            fl = ImageOps.flip(self._img)
            fl.save(image_path, format=format_)
        except PermissionError:
            LOG.error(f'Нет прав для сохранения изображения в директории {path}')
