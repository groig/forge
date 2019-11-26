import pytest

from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.text import slugify

from forge.decorators import cache_page


@pytest.fixture
def fake_view():
    def view(request):  # pylint: disable=unused-argument
        return HttpResponse('It Works')
    return view


@pytest.fixture
def fake_url():
    return '/test/url/123/'


def test_cache_page_get(rf, fake_url, fake_view):  # pylint: disable=redefined-outer-name,invalid-name
    decorated_view = cache_page(60*60)(fake_view)
    request = rf.get(fake_url)
    test_user = User('foo', 'foo@bar.com', 'bar')
    request.user = test_user
    key = f'cache-page:{request.user}:{request.method}:{slugify(request.get_full_path())}'
    response = decorated_view(request)

    assert cache.get(key) == response.content

    # Cleanup
    cache.delete_pattern(key)


def test_cache_page_post(rf, fake_url, fake_view):  # pylint: disable=redefined-outer-name,invalid-name
    decorated_view = cache_page(60*60)(fake_view)
    request = rf.get(fake_url)
    test_user = User('foo', 'foo@bar.com', 'bar')
    request.user = test_user
    request.method = 'POST'
    key = f'cache-page:{request.user}:{request.method}:{slugify(request.get_full_path())}'
    decorated_view(request)

    assert cache.get(key) is None

    # Cleanup
    cache.delete_pattern(key)
