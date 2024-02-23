from abc import ABC, abstractmethod
from PIL import Image


class AbstractFigure(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def draw(self, canvas: Image):
        pass

    @abstractmethod
    def can_be_drawn(self):
        pass
