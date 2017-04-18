from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile')
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')
    phone = models.CharField(max_length=30, blank=True, default='')
    car = models.CharField(max_length=30, blank=True, default='')
    bio = models.TextField(blank=True, default='')


def create_user_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_user_profile, sender=User)


class TravelObject(models.Model):
    start_point = models.CharField(max_length=30, blank=True, default='')
    end_point = models.CharField(max_length=30, blank=True, default='')
    luggage_size = models.CharField(max_length=30, blank=True, default='')
    price = models.CharField(max_length=30, blank=True, default='')
    about = models.TextField(blank=True, default='')
    seats_left = models.IntegerField()
    travel_time = models.FloatField()
    host = models.ForeignKey(User, null=True, related_name='travelhost')
    passengers = models.ForeignKey(User, null=True, related_name='travelpassenger')