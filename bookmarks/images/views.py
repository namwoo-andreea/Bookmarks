from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from images.forms import ImageCreateForm


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image created successfully')

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm()

    return render(request, 'images/image/create.html',
                  {'section': 'images',
                   'form': form})