from django.conf.urls import url, include
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'home$', views.home, name='home'),
    url(r'^register$', views.userRegister, name='register'),
    url(r'^login$', views.userLogin, name='login'),
    url(r'^logout$', views.userLogout, name='logout'),
    url(r'^user-profile$', views.showUserProfile, name='user-profile'),
    url(r'^user-profile/(?P<username>[a-zA-Z0-9]+)$', views.showUserProfile, name='user-profile'),
    url(r'^user-profile/fill-profile-info$', views.userFillProfileInfo, name='fill-user-profile'),
    url(r'^new-travel$', views.createTravelObject, name='new-travel'),
    url(r'^user-travels$', views.showUserTravels, name='user-travels'),
    url(r'^travels$', views.showAllTravels, name='travels'),
    url(r'^travels/(?P<travel_id>[0-9]+)/$', views.showTravelDetails, name='travel-details'),
    url(r'^travels/(?P<travel_id>[0-9]+)/save_passenger/$', views.save_passenger, name='save_passenger'),
    url(r'^travels/(?P<travel_id>[0-9]+)/leave_passenger/$', views.leave_passenger, name='leave_passenger'),
    url(r'^travels/(?P<travel_id>[0-9]+)/remove_passenger/(?P<username>[a-zA-Z0-9]+)$', views.remove_passenger, name='remove_passenger'),
]