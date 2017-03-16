from django.http import HttpResponse
from django.shortcuts import render

def users(request):
    return HttpResponse("<h1>users</h1>")

def register(request):
    jan = 'jan'
    context = {'jan': jan}
    return render(request, 'users/register.html', context)
