from decouple import config

if config('DJANGO_SETTINGS_MODULE') == 'config.settings.dev':
    from .dev import *  # pylint: disable=wildcard-import

if config('DJANGO_SETTINGS_MODULE') == 'config.settings.prod':
    from .prod import *  # pylint: disable=wildcard-import
