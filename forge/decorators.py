from typing import Any, Callable

from functools import wraps

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.utils.text import slugify


def cache_page(expiration: int) -> Callable:
    """This decorator works in replacement to Django's decorator with same name, but
    it doesn't use Django's middleware system to make cache key, so, it uses its own
    logic to do it and make possible invalidate cache.

    This decorator shouldn't be used to views with user-based data."""

    def decorator(view: Callable) -> Callable:

        @wraps(view)
        def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            key = f'cache-page:{request.user}:{request.method}:{slugify(request.get_full_path())}'
            cached = cache.get(key)
            if not cached:
                response = view(request, *args, **kwargs)
                to_cache = response.content
                # Only stores in cache if is a regular HttpResponse returning text/html
                # and the response code is 200
                if (isinstance(response, HttpResponse)
                        and getattr(response, 'mimetype', 'text/html') == 'text/html'
                        and response.status_code == 200
                        and request.method != 'POST'):
                    cache.set(key, to_cache, timeout=expiration)
                else:
                    return response
            return HttpResponse(cached or to_cache)

        return wrapper

    return decorator
