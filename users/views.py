from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from users.forms import *

def index(request):
    return HttpResponse("<h1>users</h1>")

def userRegister(request):

    form = UserForm_Register(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)

            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.save()

            return HttpResponse("<h1>registration successful</h1>")
    else:
        return render(request, 'users/register.html', {"form": form,})


def userLogin(request):

    form = UserForm_Login(request.POST or None)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponse("<h1>login success</h1>")
            else:
                return HttpResponse("<h1>login blocked</h1>")
        else:
            return HttpResponse("<h1>login error</h1>")
    else:
        return render(request, 'users/login.html', {'form':form,})

def userLogout(request):
    logout(request)
    return HttpResponse("<h1>logged out</h1>")