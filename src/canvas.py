from PIL import Image


class Canvas:
    def __init__(self, width: int, height: int, color: str = 'white'):
        self.canvas = Image.new("RGB", (width, height), "white")

    def save(self, path, format):
        self.canvas.save(format=format)