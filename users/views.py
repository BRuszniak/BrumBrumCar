from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import string
from users.forms import *
from users.models import *


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

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user.is_active:
                login(request, user)
                return redirect('/users/home')
            else:
                return redirect('/users/login')
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


def showUserProfile(request, username):

    usersReviewsList = ReviewUser.objects.filter(reviewed_user_username=username)
    user = User.objects.get(username=username)

    form = {'user': user,
            'usersReviewsList': usersReviewsList}

    return render(request, 'users/user-profile.html', form)


#@login_required(login_url = '/users/login/')
def createTravelObject(request):
    travelform = TravelForm(request.POST or None)

    if request.method == 'POST':
        if travelform.is_valid():
            travel_object = travelform.save(commit=False)
            travel_object.host = request.user
            travel_object.save()

            return render(request, "users/new-travel.html", {"travelform": travelform, })
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

    search_start = request.GET.get("search_start")
    search_end = request.GET.get("search_end")

    if search_start and search_end:
        travels_list = TravelObject.objects.filter(
            Q(start_point=search_start),
            Q(end_point=search_end)
        ).distinct()
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
    reviewForm = ReviewUserForm(request.POST or None)

    if 'reviewForm' in request.POST:
        reviewForm = ReviewUserForm(request.POST or None)
        saveReview(reviewForm, request.user)
    elif 'start' in request.POST:
        travel.travel_state = "IN_PROGRESS"
        travel.save()
    elif 'end' in request.POST:
        removeTravelObject(travel_id)

    contex = {
        'travel': travel,
        'is_signed': is_signed,
        'reviewForm': reviewForm
    }

    return render(request, 'users/travel-details.html', contex)

def removeTravelObject(travel_id):

    travelToDelete = TravelObject.objects.get(pk=travel_id)
    travelToDelete.delete()
    return redirect('/users/')


def saveReview(reviewForm, user):

    if reviewForm.is_valid():
        reviewObject = reviewForm.save(commit=False)
        reviewObject.reviewer_username = user.username
        reviewObject.save()
    else:
        return HttpResponse("<h1>reviewForm form is not valid</h1>")



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


#@login_required(login_url = '/users/login/')
def leave_passenger(request, travel_id):

    try:
        travel = TravelObject.objects.get(pk=travel_id)
    except TravelObject.DoesNotExist:
        raise Http404("Travel does not exist")

    travel.passengers.remove(request.user)
    travel.seats_left += 1
    travel.save()

    return redirect('/users/travels/'+travel_id)


#@login_required(login_url = '/users/login/')
def remove_passenger(request, travel_id, username):

    try:
        travel = TravelObject.objects.get(pk=travel_id)
    except TravelObject.DoesNotExist:
        raise Http404("Travel does not exist")

    try:
        us = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Passenger does not exist")

    if request.user == travel.host:
        travel.passengers.remove(us)
        travel.seats_left += 1
        travel.save()

    return redirect('/users/travels/'+travel_id)
