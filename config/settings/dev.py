"""
Development settings for forge project
"""

from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS: list = []

# Application definition

INSTALLED_APPS += [
    'django_extensions',
]

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list = []

# Django Debug Toolbar Settings
INTERNAL_IPS = ['127.0.0.1']

TEST_RUNNER = 'config.test_runner.PytestTestRunner'

JQUERY_URL = ''

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
)
