from django.contrib import admin
from .models import Profile, TobToken

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type')

@admin.register(TobToken)
class TobTokenAdmin(admin.ModelAdmin):
    list_display = ('username', 'server', 'is_active')