from django.contrib import admin
from .models import GoogleCalendarToken

@admin.register(GoogleCalendarToken)
class GoogleCalendarTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'expires_at')