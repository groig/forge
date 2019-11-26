from typing import Dict
from django.conf import settings
from django.http import HttpRequest


def debug_features(request: HttpRequest) -> Dict[str, bool]:  # pylint: disable=unused-argument
    return {'LOAD_DEBUG_FEATURES': settings.DEBUG}
