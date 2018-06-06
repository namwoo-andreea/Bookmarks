from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm, UserRegistrationForm


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
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',
                  {'user_form': user_form})


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
