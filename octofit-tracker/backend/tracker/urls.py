from django.urls import path
from .views import ActivityListCreateAPIView, TeamListCreateAPIView, TeamRetrieveUpdateDestroyAPIView, UserListAPIView

urlpatterns = [
    path('activities/', ActivityListCreateAPIView.as_view(), name='activity-list-create'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('teams/', TeamListCreateAPIView.as_view(), name='team-list-create'),
    path('teams/<int:pk>/', TeamRetrieveUpdateDestroyAPIView.as_view(), name='team-detail'),
]
