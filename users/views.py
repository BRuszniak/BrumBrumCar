from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


from users.forms import *

def index(request):
    return HttpResponse("<h1>users</h1>")

def register(request):

    form = UserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponse("<h1>users</h1>")
    else:
        context = {
          "form": form,
        }
    return render(request, 'users/register.html', context)