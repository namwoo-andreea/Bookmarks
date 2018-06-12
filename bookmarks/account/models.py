from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile/%y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {0}'.format(self.user.username)


class Contact(models.Model):
    user_from = models.ForeignKey(User,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,
                                      db_index=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return '{0} follows {1}'.format(self.user_from,
                                        self.user_to)


User.add_to_class('following', models.ManyToManyField('self',
                                                      through=Contact,
                                                      related_name='followers',
                                                      symmetrical=False))
