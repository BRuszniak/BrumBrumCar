from django.contrib.auth.models import User
from django import forms
from users.models import UserProfile, TravelObject, ReviewUser


class UserFormRegister(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserFormLogin(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserFormProfile(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'phone', 'car', 'bio']


class TravelForm(forms.ModelForm):

    class Meta:
        model = TravelObject
        fields = ['start_point', 'end_point', 'luggage_size', 'price', 'about', 'seats_left', 'travel_time']


class ReviewUserForm(forms.ModelForm):

    class Meta:
        model = ReviewUser
        fields = ['reviewed_user_username', 'body', 'rating']