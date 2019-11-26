from django.apps import AppConfig


class ForgeConfig(AppConfig):
    name = 'forge'

    def ready(self) -> None:
        from . import handlers  # pylint: disable=unused-variable
