from django.contrib import admin
from .models import User, Advertisement

class UserModelAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'phone_number'
    ]
    search_fields = ['email', 'full_name']

class AdvertisementModelAdmin(admin.ModelAdmin):
    list_display = [
        'author', 'title', 'created_at'
    ]

admin.site.register(User, UserModelAdmin)
admin.site.register(Advertisement, AdvertisementModelAdmin)

