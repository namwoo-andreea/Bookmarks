from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from actions.models import Action
from actions.utils import create_action
from common.decorators import ajax_required
from .models import Profile, Contact
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm

User = get_user_model()


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        # If user is following others, display only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')[:10]

    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})


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
            # Create actions for activity stream
            create_action(request.user, 'has created an account')
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
        return render(request, 'account/login.html',
                      {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'account/logout.html')


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/detail.html',
                  {'section': 'people',
                   'user': user})


@ajax_required
@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                # Create actions for activity stream
                create_action(request.user, 'follows', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})
