from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()


class Image(models.Model):
    user = models.ForeignKey(User,
                             related_name='images_bookmarked',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(User,
                                        related_name='images_liked',
                                        blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
