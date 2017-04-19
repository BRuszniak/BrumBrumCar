from django.conf.urls import url, include
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'home$', views.home, name='home'),
    url(r'^register$', views.userRegister, name='register'),
    url(r'^login$', views.userLogin, name='login'),
    url(r'^logout$', views.userLogout, name='logout'),
    url(r'^user-profile$', views.showUserProfile, name='user-profile'),
    url(r'^user-profile/fill-profile-info$', views.userFillProfileInfo, name='fill-user-profile'),
    url(r'^new-travel$', views.createTravelObject, name='new-travel'),
    url(r'^user-travels$', views.showUserTravels, name='user-travels'),
    url(r'^travels$', views.showAllTravels, name='travels'),
    url(r'^travels/(?P<travel_id>[0-9]+)/$', views.showTravelDetails, name='travel-details'),
]