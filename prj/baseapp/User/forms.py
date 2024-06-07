from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserSignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Username",
                "type": "text"
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Email Address",
                "type": "email"
            }
        )
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Password",
                "type": "password"
            }
        )
    )

    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Confirm Password",
                "type": "password"
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Email Address",
                "type": "email"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Password",
                "type": "password"
            }
        )
    )