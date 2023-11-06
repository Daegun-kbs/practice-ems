from django import forms
from django.contrib.auth.forms import UserCreationForm
from common.models import CustomUser


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    phone = forms.CharField(label="핸드폰")

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "email", "phone")