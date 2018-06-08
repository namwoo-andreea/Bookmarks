import os
from urllib import request
from urllib.parse import urlparse

from django import forms
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        parsed_url = urlparse(url)
        extension = os.path.splitext(parsed_url.path)
        if extension not in valid_extensions:
            raise forms.ValidationError('The given url does not '
                                        'match valid image extension')
        return url

    def save(self, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        parsed_url = urlparse(image_url)
        extension = os.path.splitext(parsed_url.path)
        image_name = '{0}.{1}'.format(slugify(image.title), extension)

        # Download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name, content=response.read(), save=False)

        if commit:
            image.save()
        return image