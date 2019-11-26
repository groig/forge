from django.core.cache import cache
from django.db.models import Model


def acquire_lock(user: Model, resource: Model) -> None:
    key = f'lock:{resource.pk}'
    if not cache.set(key, user.pk, 60 * 15, nx=True):
        raise ResourceAlreadyBlocked('El recurso se encuentra bloqueado por otra persona.')


def release_lock(user: Model, resource: Model) -> None:
    key = f'lock:{resource.pk}'
    user_that_locked = cache.get(key)
    if user_that_locked:
        if user.pk == user_that_locked:
            cache.delete_pattern(key)
        else:
            raise UserDoesNotOwnTheLock('Este recurso no fue bloqueado por el usuario actual.')


class ResourceAlreadyBlocked(Exception):
    pass


class UserDoesNotOwnTheLock(Exception):
    pass
