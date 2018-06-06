from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .models import Profile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but not saving it yet.
            new_user = user_form.save(commit=False)
            # Set password with cleaned_data from form.
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save user object using its save() method.
            new_user.save()
            # Create user profile.
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile update successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':
        # Create a form with data from request.POST.
        form = LoginForm(request.POST)
        # Check a validity of the form
        if form.is_valid():
            # Assign cleaned data which created in process of is_valid()
            cd = form.cleaned_data
            # Authenticate user with cleaned data, return user or None
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            # Check user is authenticated and is activated
            if user is not None:
                if user.is_active:
                    # Login user, sets user in the current session
                    login(request, user)
                    return HttpResponse('Successfully Login')
                else:
                    return HttpResponse('Disable account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm(request.POST)
        return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'account/logout.html')
