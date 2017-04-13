from django.contrib import admin
from users.models import UserProfile
from users.models import TravelObject

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(TravelObject)