from kivy.uix.button import Button
from kivy.uix.image import Image


class ImageButton(Button):
    def __init__(self, image_source, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)

        self.image = Image(source=image_source, allow_stretch=True)
        self.add_widget(self.image)

        self.bind(size=self._update_image_size)
        self.bind(pos=self._update_image_position)
        self.background_color = (0, 0, 0, 0)


    def _update_image_size(self, instance, value):
        """Update image size when the button's size changes."""
        self.image.size = self.size

    def _update_image_position(self, instance, value):
        """Update image position when the button's position changes."""
        self.image.pos = self.pos
