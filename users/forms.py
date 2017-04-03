from django.contrib.auth.models import User
from django import forms
from users.models import UserProfile


class UserForm_Register(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserForm_Login(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class UserForm_Profile(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'phone', 'car', 'bio']

