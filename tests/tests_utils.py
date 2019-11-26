import pytest

from django.core.cache import cache

from forge.utils import (acquire_lock, release_lock,
                      ResourceAlreadyBlocked, UserDoesNotOwnTheLock)


class ThingWithPk:  # pylint: disable=too-few-public-methods
    def __init__(self, pk):
        self.pk = pk  # pylint: disable=invalid-name


@pytest.fixture
def fake_user():
    return ThingWithPk('123')


@pytest.fixture
def fake_resource():
    return ThingWithPk('456')


def test_acquire_lock_success(fake_user, fake_resource):  # pylint: disable=redefined-outer-name
    key = f'lock:{fake_resource.pk}'

    # Intenta adquirir el lock
    acquire_lock(fake_user, fake_resource)

    # Verifica que se obtuvo con éxito
    assert cache.get(key) == fake_user.pk

    # Cleanup
    cache.delete_pattern(key)


def test_acquire_lock_raises(fake_user, fake_resource):  # pylint: disable=redefined-outer-name
    key = f'lock:{fake_resource.pk}'

    # Crea un lock a mano
    cache.set(key, fake_user.pk)

    # Verifica que no se pueda obtener si ya está bloqueado
    with pytest.raises(ResourceAlreadyBlocked):
        acquire_lock(fake_user, fake_resource)

    # Cleanup
    cache.delete_pattern(key)


def test_release_lock_success(fake_user, fake_resource):  # pylint: disable=redefined-outer-name
    key = f'lock:{fake_resource.pk}'

    # Crea un lock a mano
    cache.set(key, fake_user.pk)

    # Intenta liberar el lock
    release_lock(fake_user, fake_resource)

    # Verifica que se liberó con éxito
    assert cache.get(key) is None

    # Cleanup
    cache.delete_pattern(key)


def test_release_lock_raises(fake_user, fake_resource):  # pylint: disable=redefined-outer-name
    key = f'lock:{fake_resource.pk}'

    # Crea un lock a mano
    cache.set(key, fake_user.pk)

    # Verifica que no se pueda liberar si el usuario es diferente
    fake_user.pk = '789'
    with pytest.raises(UserDoesNotOwnTheLock):
        release_lock(fake_user, fake_resource)

    # Cleanup
    cache.delete_pattern(key)
