import logging
import sys
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler(sys.stdout))



class AbstractFigure(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        self._figure_params = {
            'fill': kwargs.get('Color', 'white'),
            'outline': kwargs.get('outline', 'black'),
            'width': kwargs.get('line_width', 1)
        }

    @abstractmethod
    def draw(self, image_draw: ImageDraw):
        """
        Рисовать фигуру можно только если она еще не была нарисована.
        """
        pass


class Circle(AbstractFigure):
    def __init__(self, **kwargs):
        try:
            self._X_center = kwargs['X_center']
            self._Y_center = kwargs['Y_center']
            self._radius = kwargs['Radius']
        except KeyError:
            LOG.error(f'Не соблюден входной формат для фигуры {self.__class__.__name__}')

        super().__init__(**kwargs)

    def draw(self, image_draw: ImageDraw):
        x0 = self._X_center - self._radius
        y0 = self._Y_center - self._radius
        x1 = self._X_center + self._radius
        y1 = self._Y_center + self._radius

        image_draw.ellipse([(x0, y0), (x1, y1)], **self._figure_params)


class Rectangle(AbstractFigure):
    def __init__(self, **kwargs):
        try:
            self._X_upper_left = kwargs['X_upper_left']
            self._Y_upper_left = kwargs['Y_upper_left']
            self._X_lower_right = kwargs['X_lower_right']
            self._Y_lower_right = kwargs['Y_lower_right']
        except KeyError:
            LOG.error(f'Не соблюден входной формат для фигуры {self.__class__.__name__}')

        super().__init__(**kwargs)

    def draw(self, image_draw: ImageDraw):

        x_left = self._X_upper_left
        x_right = self._X_lower_right
        y_left = self._Y_lower_right
        y_right = self._Y_upper_left

        image_draw.rectangle(
            ((x_left, y_left),
            (x_right, y_right)),
            **self._figure_params)


class Square(AbstractFigure):
    def __init__(self, **kwargs):
        try:
            self._X_upper_left = kwargs['X_upper_left']
            self._Y_upper_left = kwargs['Y_upper_left']
            self._side_length = kwargs['side_length']
        except KeyError:
            LOG.error(f'Не соблюден входной формат для фигуры {self.__class__.__name__}')

        super().__init__(**kwargs)

    def draw(self, image_draw: ImageDraw):

        x_left = self._X_upper_left - self._side_length
        x_right = self._X_upper_left + self._side_length
        y_left = self._Y_upper_left - self._side_length
        y_right = self._Y_upper_left + self._side_length

        image_draw.rectangle(
            ((x_left, y_left),
            (x_right, y_right)),
            **self._figure_params)


class Triangle(AbstractFigure):
    def __init__(self, **kwargs):
        try:
            shape = kwargs['Shape']
            self.point_1_x = shape[0]['Point']['X']
            self.point_1_y = shape[0]['Point']['Y']

            self.point_2_x = shape[1]['Point']['X']
            self.point_2_y = shape[1]['Point']['Y']

            self.point_3_x = shape[2]['Point']['X']
            self.point_3_y = shape[2]['Point']['Y']

        except KeyError:
            LOG.error(f'Не соблюден входной формат для фигуры {self.__class__.__name__}')

        super().__init__(**kwargs)

    def draw(self, image_draw: ImageDraw):
        image_draw.polygon([(self.point_1_x, self.point_1_y),
                            (self.point_2_x, self.point_2_y),
                            (self.point_3_x, self.point_3_y)],
                           **self._figure_params)
