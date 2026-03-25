from django.contrib import admin
from .models import Activity, Team


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'duration_minutes', 'distance_km', 'calories_burned', 'timestamp')
    list_filter = ('type', 'timestamp')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    filter_horizontal = ('members',)
