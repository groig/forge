# Create your tasks here

from django_rq import job
from django.core.cache import cache


@job
def vanish_pattern_from_cache(pattern: str) -> None:
    cache.delete_pattern(pattern)

@job
def release_all_locks_of_user(user_id: str) -> None:
    for key in cache.iter_keys('lock:*'):
        if str(cache.get(key)) == user_id:
            cache.delete_pattern(key)
