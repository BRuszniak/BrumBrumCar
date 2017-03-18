from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')
    phone = models.CharField(max_length=30, blank=True, default='')
    car =  models.CharField(max_length=30, blank=True, default='')
    bio = models.TextField(blank=True, default='')

