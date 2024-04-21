from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """
    Форма регитсрации нового пользователя
    """
    email = forms.EmailField(max_length=200,)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )


class UserProfileForm(UserChangeForm):
    """
    Форма просмотра и редактирования профиля пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', )

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserForgotPasswordForm(PasswordResetForm):
    """
    Запрос на восстановление пароля
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserSetNewPasswordForm(SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })