from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser, Event, Participant, EventImage, UserFollow, EventInteraction
from django.forms import Textarea
from django.db import models

# Event Admin
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('title', 'host_owner', 'location', 'date_start', 'date_closed', 'is_private', 'open_status')
    list_filter = ('is_private', 'open_status', 'date_start', 'date_closed', 'date_created')
    fieldsets = (
        ('Labeling', {'fields': ('title', 'description', 'tags', 'host_owner')}),
        ('Media', {'fields': ('thumbnail', 'images')}),
        ('Location', {'fields': ('location', 'distance', 'latitude', 'longitude')}),
        ('Properties', {'fields': ('is_private', 'needs_id', 'open_status', 'price', 'rating', 'seats')}),
        ('Date logs', {'fields': ('date_created', 'date_start', 'date_closed')})
        )
    search_fields = ('title', 'description', 'location', 'host_owner')
    ordering = ('-date_start',)

# AppUser Admin
class AppUserAdmin(admin.ModelAdmin):
    model = AppUser
    list_display = ('username', 'fullname', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        ('Authentication', {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('fullname', 'email', 'bio', 'mobile_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Date logs', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fullname', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 60})},
    }

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventImage)
admin.site.register(Participant)
admin.site.register(EventInteraction)
admin.site.register(UserFollow)