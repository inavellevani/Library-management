from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'personal_number', 'birth_date', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
