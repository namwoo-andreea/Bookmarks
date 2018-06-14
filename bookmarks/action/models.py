from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,
                                      db_index=True)

    class Meta:
        ordering = ('-created_at', )
