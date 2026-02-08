from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        error_messages={"required": "Поле не заполнено"},
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "example"}),
    )
    email = forms.EmailField(
        label="E-mail",
        error_messages={"required": "Поле не заполнено"},
        widget=forms.EmailInput(attrs={"class": "input", "placeholder": "you@example.com"}),
    )
    password1 = forms.CharField(
        label="Пароль",
        error_messages={"required": "Поле не заполнено"},
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Минимум 8 символов", "minlength": "8"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        error_messages={"required": "Поле не заполнено"},
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Повторите пароль", "minlength": "8"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        error_messages={"required": "Поле не заполнено"},
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "your_username"}),
    )
    password = forms.CharField(
        label="Пароль",
        error_messages={"required": "Поле не заполнено"},
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "••••••••"}),
    )
