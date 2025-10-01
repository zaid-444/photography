from django.contrib import admin
from .models import UserProfile, PhotographerProfile,Booking,Notification

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_approved']
    list_filter = ['role', 'is_approved']
    search_fields = ['user__username']

@admin.register(PhotographerProfile)
class PhotographerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialty', 'location']

admin.site.register(Booking)
admin.site.register(Notification)
