from django.contrib.auth.models import User
from django.db import models


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    type = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    calories_burned = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} {self.type} ({self.duration_minutes}min)"


class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='owned_teams')
    members = models.ManyToManyField('auth.User', related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
