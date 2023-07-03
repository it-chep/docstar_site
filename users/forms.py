from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    email = forms.CharField(label='Email', initial='',)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'password_input', 'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'password2_input', 'placeholder': 'Повторите пароль'}))
    Username = None

    class Meta:
        Username = None
        model = CustomUser
        fields = ('email', )

    # def get_email_account(self, response):
    #     email = response.GET.get("email")
    #     return email


class CustomUserChangeForm(UserChangeForm):
    email = forms.CharField(label='Email', initial='')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'password_input'}))

    class Meta:
        model = CustomUser
        fields = ('email', )


class LoginUserForm(AuthenticationForm):
    email = forms.CharField(label='Email', initial='')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = CustomUser
        fields = ('email', )
