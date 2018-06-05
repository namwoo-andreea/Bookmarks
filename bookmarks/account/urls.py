from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('forgot_password', auth_views.PasswordResetView.as_view(), name='forgot-password'),
    path('forgot_password/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='forgot-password-done'),
    path('forgot_password/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='forgot-password-confirm'),
    path('forgot_password/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='forgot-password-complete'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
]
