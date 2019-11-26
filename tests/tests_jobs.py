import uuid

from django.core.cache import cache

from forge.jobs import release_all_locks_of_user, vanish_pattern_from_cache


def test_vanish_pattern_from_cache():
    pattern = uuid.uuid4()
    cache.set(pattern, uuid.uuid4())
    vanish_pattern_from_cache(pattern)
    assert cache.get(pattern) is None


def test_release_all_locks_of_user():
    user_id = uuid.uuid4()
    lock = uuid.uuid4()
    lock1 = uuid.uuid4()
    cache.set(f'lock:{lock}', user_id)
    cache.set(f'lock:{lock1}', user_id)
    release_all_locks_of_user(str(user_id))
    for key in cache.keys('lock:*'):
        assert cache.get(key) != user_id
