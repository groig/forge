import pytest

from forge.templatetags.forge_tags import active_url


ACTIVE = 'class="active"'
INACTIVE = ''
UUID = '8e9d5d10-bfb1-4f73-9da1-94dabb94a4ff'
SLUG = 'some-slug'
PATH_INDEX = '/forge/'
NAME_INDEX = 'forge:index'
NAME_DETAILS = 'forge:structure_details'
PATH_DETAILS = f'/forge/s/{SLUG}/{UUID}/'


@pytest.mark.parametrize('path,url_name,slug,uuid,result', [
    (PATH_INDEX, NAME_INDEX, None, None, ACTIVE),
    (PATH_DETAILS, NAME_DETAILS, 'some-slug', UUID, ACTIVE),
    (PATH_INDEX, NAME_INDEX, 'some-slug', UUID, INACTIVE),
    (PATH_DETAILS, NAME_DETAILS, None, None, INACTIVE),
])  # pylint: disable=invalid-name
def test_active_url_active(rf, path, url_name, slug, uuid, result):
    request = rf.get(path)
    assert active_url({'request': request}, url_name, slug, uuid) == result
