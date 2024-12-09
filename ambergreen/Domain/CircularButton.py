from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color

class CircularButton(Button):
    def __init__(self, button_size=(100, 100), **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = button_size
        self.background_color = (0, 0, 0, 0)

        self.bind(pos=self.update_circle_position)
        self.bind(size=self.update_circle_position)

        with self.canvas.before:
            Color(1, 0, 0, 1)
            self.button_circle = Ellipse(pos=self.pos, size=self.size)

    def update_circle_position(self, instance, value):
        """Update the position of the circle when the button's position or size changes."""
        self.button_circle.pos = self.pos
        self.button_circle.size = self.size
