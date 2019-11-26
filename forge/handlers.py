from typing import Any

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http import HttpRequest

from . import jobs
from .models import BaseModel, Data, Structure


@receiver(user_logged_out)
def post_logout_cleaning(sender: Any, request: HttpRequest, user: User, **kwargs: Any) -> None:  # pylint: disable=unused-argument
    '''
    Remove all possible locks held by an user on logout
    '''
    if sender:
        jobs.release_all_locks_of_user.delay(str(user.id))


def post_save_cleaning(sender: Any, instance: BaseModel, created: bool, *args: Any, **kwargs: Any) -> None:  # pylint: disable=unused-argument
    if not created:
        jobs.vanish_pattern_from_cache.delay(f'*{instance.pk}*')


post_save.connect(post_save_cleaning, sender=Data)
post_save.connect(post_save_cleaning, sender=Structure)


def post_delete_cleaning(sender: Any, instance: BaseModel, *args: Any, **kwargs: Any) -> None:  # pylint: disable=unused-argument
    jobs.vanish_pattern_from_cache.delay(f'*{instance.pk}*')
    if sender == Structure:
        for data in Data.objects.filter(structure_id=instance.pk):
            jobs.vanish_pattern_from_cache.delay(f'*{data.pk}*')


post_delete.connect(post_delete_cleaning, sender=Data)
post_delete.connect(post_delete_cleaning, sender=Structure)
