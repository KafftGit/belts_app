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
        error_messages={
            "required": "Поле не заполнено",
            "invalid": "Введите корректный адрес электронной почты",
        },
        widget=forms.EmailInput(attrs={"class": "input", "placeholder": "you@example.com"}),
    )
    password1 = forms.CharField(
        label="Пароль",
        error_messages={"required": "Поле не заполнено"},
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Минимум 8 символов",
                "minlength": "8",
            }
        ),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        error_messages={"required": "Поле не заполнено"},
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Повторите пароль",
                "minlength": "8",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Убираем стандартные help_text Django на английском
        self.fields["username"].help_text = ""
        self.fields["email"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с такой электронной почтой уже существует")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if password:
            if len(password) < 8:
                raise forms.ValidationError("Пароль должен содержать не менее 8 символов")

            if password.isdigit():
                raise forms.ValidationError("Пароль не должен состоять только из цифр")

            common_passwords = {
                "12345678",
                "123456789",
                "qwerty123",
                "password",
                "password123",
                "admin123",
                "11111111",
                "00000000",
            }
            if password.lower() in common_passwords:
                raise forms.ValidationError("Пароль слишком простой")

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        if commit:
            user.save()
        return user


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

    error_messages = {
        "invalid_login": "Неверное имя пользователя или пароль",
        "inactive": "Этот аккаунт отключён",
    }