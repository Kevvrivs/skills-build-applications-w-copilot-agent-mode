from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tracker.models import Team, Activity, WorkoutSuggestion

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Clear existing data
        Activity.objects.all().delete()
        Team.objects.all().delete()
        # Djongo workaround: delete non-superusers in Python loop
        User.objects.filter(is_superuser=False).delete()
        WorkoutSuggestion.objects.all().delete()

        # Create users
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com'},
            {'username': 'superman', 'email': 'superman@dc.com'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
        ]
        marvel_users = [User.objects.create_user(**u, password='password') for u in marvel_heroes]
        dc_users = [User.objects.create_user(**u, password='password') for u in dc_heroes]

        # Create teams
        marvel_team = Team.objects.create(name='Team Marvel', owner=marvel_users[0])
        marvel_team.members.set(marvel_users)
        dc_team = Team.objects.create(name='Team DC', owner=dc_users[0])
        dc_team.members.set(dc_users)

        # Create activities
        for user in marvel_users + dc_users:
            Activity.objects.create(user=user, type='run', duration_minutes=30, distance_km=5, calories_burned=300)
            Activity.objects.create(user=user, type='cycle', duration_minutes=60, distance_km=20, calories_burned=600)

        # Create workout suggestions
        WorkoutSuggestion.objects.create(
            name='Morning Run', description='Easy 5km run', difficulty='easy', target_duration_minutes=30, target_distance_km=5, created_by=marvel_users[0]
        )
        WorkoutSuggestion.objects.create(
            name='Hero Cycle', description='Challenging 20km cycle', difficulty='hard', target_duration_minutes=60, target_distance_km=20, created_by=dc_users[0]
        )

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
