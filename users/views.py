from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm, UserSetNewPasswordForm, UserForgotPasswordForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.send_activation_email(user)
        return HttpResponseRedirect(self.get_success_url())

    def send_activation_email(self, user):
        mail_subject = 'Activate your account.'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"http://127.0.0.1:8000/users/activate/{uid}/{token}/"
        message = render_to_string('users/activation_email.html', {
            'user': user,
            'activation_link': activation_link,
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

    def get_success_url(self):
        return self.success_url


class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.is_active = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Method not allowed', status=405)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте:
    Функционал для запроса пароля, где мы вводим свой email адрес.
    Используем форму UserForgotPasswordForm.
    Наследуемся от PasswordResetView представления, встроенного в Django.
    Указываем соответствующие шаблоны как для формы, так и для писем.
    Подмешиваем миксин SuccessMessageMixin для оповещения пользователя
    об успешной отправке письма с инструкцией по восстановлению пароля.
    """
    form_class = UserForgotPasswordForm
    template_name = 'users/registration/user_password_reset.html'
    success_url = reverse_lazy('catalog:home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    Функционал для ввода нового пароля.
    Используем форму UserSetNewPasswordForm.
    Наследуемся от PasswordResetConfirmView представления, встроенного в Django.
    Указываем соответствующие шаблоны для формы.
    Подмешиваем миксин SuccessMessageMixin для оповещения пользователя об успешной смене пароля.
    """
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('catalog:home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

