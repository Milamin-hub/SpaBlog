from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'state_id', 'photo')

admin.site.register(Profile, ProfileAdmin)