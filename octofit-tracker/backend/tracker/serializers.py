from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Activity, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'user', 'type', 'duration_minutes', 'distance_km', 'calories_burned', 'timestamp']


class TeamSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members', 'created_at']

