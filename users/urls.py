from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, ActivateView, UserForgotPasswordView, UserPasswordResetConfirmView

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('activate/<str:uidb64>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('password_reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set_new_password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
# fttb100983 AiMobil@yandex.ru