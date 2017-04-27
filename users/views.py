from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import string
from users.forms import *
from users.models import *


def index(request):
    return HttpResponse("<h1>users</h1>")

def home(request):
    return render(request, 'users/home.html')


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
                return redirect('/users/home')
            else:
                return redirect('/users/login')
        else:
            return redirect('/users/login')
    else:
        return render(request, 'users/login.html', {'form': form, })


def userLogout(request):
    logout(request)
    return redirect('/users/home')


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


#@login_required(login_url = '/users/login/')
def createTravelObject(request):
    travelform = TravelForm(request.POST or None)

    if request.method == 'POST':
        if travelform.is_valid():
            travel_object = travelform.save(commit=False)
            travel_object.host = request.user
            travel_object.save()

            return HttpResponse("<h1>Travel form created</h1>")
        else:
            return HttpResponse("<h1>Travel form is not valid</h1>")
    else:
        return render(request, "users/new-travel.html", {"travelform": travelform, })


#@login_required(login_url = '/users/login/')
def showUserTravels(request):
    travels_hosted = TravelObject.objects.filter(host=request.user)
    travels_passenger = request.user.travelpassenger.all()

    contex = {
        'travels_hosted': travels_hosted,
        'user': request.user,
        'travels_passenger': travels_passenger
    }
    return render(request, 'users/user-travels.html', contex)


def showAllTravels(request):

    travel_search = request.GET.get("search")

    if travel_search:
        travels_list = TravelObject.objects.filter(start_point=travel_search)
    else:
        travels_list = TravelObject.objects.all()

    contex = {
        'travels_list': travels_list
    }
    return render(request, 'users/travels.html', contex)


#@login_required(login_url = '/users/login/')
def showTravelDetails(request, travel_id):

    try:
        travel = TravelObject.objects.get(pk=travel_id)
    except TravelObject.DoesNotExist:
        raise Http404("Travel does not exist")

    is_signed = request.user.travelpassenger.filter(id=travel_id).exists()

    contex = {
        'travel': travel,
        'is_signed': is_signed
    }

    return render(request, 'users/travel-details.html', contex)


#@login_required(login_url = '/users/login/')
def save_passenger(request, travel_id):

    try:
        travel = TravelObject.objects.get(pk=travel_id)
    except TravelObject.DoesNotExist:
        raise Http404("Travel does not exist")

    if travel.seats_left - 1 >= 0:
        travel.passengers.add(request.user)
        travel.seats_left -= 1
        travel.save()
    else:
        return Http404("No available seats")

    return redirect('/users/travels/'+travel_id)
