import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Action


def create_action(user, verb, target=None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    duplicated_actions = Action.objects.filter(id=user.id,
                                               verb=verb,
                                               created_at__gte=last_minute)

    if target:
        target_content_type = ContentType.objects.get_for_model(target)
        duplicated_actions = duplicated_actions.filter(target_content_type=target_content_type,
                                                       target_id=target.id)
    if not duplicated_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False