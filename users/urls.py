from django.conf.urls import url, include
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.userRegister, name='register'),
    url(r'^login$', views.userLogin, name='login'),
    url(r'^logout', views.userLogout, name='logout'),
]
