from django.contrib import admin
from users.models import UserProfile
from users.models import TravelObject
from users.models import ReviewUser

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(TravelObject)
admin.site.register(ReviewUser)