from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password-reset-done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password-reset-complete'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/list/', views.user_list, name='user-list'),
    path('users/follow/', views.user_follow, name='user-follow'),
    path('users/detail/<username>/', views.user_detail, name='user-detail'),
]
