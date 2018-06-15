from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(ContentType,
                                            related_name='target',
                                            on_delete=models.CASCADE,
                                            blank=True,
                                            null=True)
    target_object_id = models.PositiveIntegerField(db_index=True,
                                                   blank=True,
                                                   null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    created_at = models.DateTimeField(auto_now_add=True,
                                      db_index=True)

    class Meta:
        ordering = ('-created_at',)
