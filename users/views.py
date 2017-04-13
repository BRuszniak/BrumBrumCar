from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import string
from users.forms import *


def index(request):
    return HttpResponse("<h1>users</h1>")


def userRegister(request):

    form = UserFormRegister(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)

            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.save()

            return HttpResponse("<h1>registration successful</h1>")
    else:
        return render(request, 'users/register.html', {"form": form, })


def userLogin(request):

    form = UserFormLogin(request.POST or None)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("<h1>login success</h1>")
            else:
                return HttpResponse("<h1>login blocked</h1>")
        else:
            return HttpResponse("<h1>login error</h1>")
    else:
        return render(request, 'users/login.html', {'form': form, })


def userLogout(request):
    logout(request)
    return HttpResponse("<h1>logged out</h1>")


#@login_required(login_url = '/users/login/')
def userFillProfileInfo(request):

    if request.method == 'POST':
        profileInfoForm = UserFormProfile(request.POST, instance=request.user.userprofile)

        if profileInfoForm.is_valid():
            profileInfoForm.save()
            return HttpResponse("<h1>Profile Updated</h1>")
        else:
            return HttpResponse("<h1>profileInfoForm is not valid</h1>")
    else:
        profileInfoForm = UserFormProfile(instance=request.user.userprofile)
        return render(request, 'users/fill-profile-info.html', {'profileInfoForm': profileInfoForm, })


#@login_required(login_url = '/users/login/')
def showUserProfile(request):
    form = {'user': request.user}
    return render(request, 'users/user-profile.html', form)