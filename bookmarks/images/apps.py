from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def __init__(self):
        import images.signals
