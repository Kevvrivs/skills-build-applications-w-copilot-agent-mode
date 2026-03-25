from django.urls import path
from .views import (
    ActivityListCreateAPIView,
    TeamLeaderboardAPIView,
    TeamListCreateAPIView,
    TeamRetrieveUpdateDestroyAPIView,
    UserListAPIView,
    WorkoutSuggestionListCreateAPIView,
    WorkoutSuggestionRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('activities/', ActivityListCreateAPIView.as_view(), name='activity-list-create'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('teams/', TeamListCreateAPIView.as_view(), name='team-list-create'),
    path('teams/<int:pk>/', TeamRetrieveUpdateDestroyAPIView.as_view(), name='team-detail'),
    path('leaderboard/', TeamLeaderboardAPIView.as_view(), name='team-leaderboard'),
    path('workout-suggestions/', WorkoutSuggestionListCreateAPIView.as_view(), name='workout-suggestion-list-create'),
    path('workout-suggestions/<int:pk>/', WorkoutSuggestionRetrieveUpdateDestroyAPIView.as_view(), name='workout-suggestion-detail'),
]
