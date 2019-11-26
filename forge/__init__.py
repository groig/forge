from django.conf import settings

from .registries import modules

default_app_config = 'forge.apps.ForgeConfig'

modules.autodiscover(settings.INSTALLED_APPS)
