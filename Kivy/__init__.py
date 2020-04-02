from kivymd.app import MDApp
from kivy.lang import Builder


class Booked(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Teal"

    def build(self):
        return Builder.load_file("widgets.kv")


Booked().run()