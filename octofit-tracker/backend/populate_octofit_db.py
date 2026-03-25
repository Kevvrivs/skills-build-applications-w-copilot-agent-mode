import pymongo
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['octofit_db']

# Clear collections
for col in ['auth_user', 'tracker_team', 'tracker_activity', 'tracker_workoutsuggestion', 'tracker_team_members']:
    db[col].delete_many({})

# Insert users

# Assign unique integer IDs for users
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
users = []
user_id_counter = 1
for hero in marvel_heroes + dc_heroes:
    user = {
        'id': user_id_counter,
        'password': '',
        'last_login': None,
        'is_superuser': False,
        'username': hero['username'],
        'first_name': '',
        'last_name': '',
        'email': hero['email'],
        'is_staff': False,
        'is_active': True,
        'date_joined': datetime.utcnow(),
    }
    users.append(user)
    user_id_counter += 1
user_ids = db.auth_user.insert_many(users).inserted_ids
marvel_user_ids = [u['id'] for u in users[:3]]
dc_user_ids = [u['id'] for u in users[3:]]

# Insert teams

# Assign unique integer IDs for teams
marvel_team = {
    'id': 1,
    'name': 'Team Marvel',
    'owner_id': marvel_user_ids[0],
    'created_at': datetime.utcnow(),
}
dc_team = {
    'id': 2,
    'name': 'Team DC',
    'owner_id': dc_user_ids[0],
    'created_at': datetime.utcnow(),
}
marvel_team_id = db.tracker_team.insert_one(marvel_team).inserted_id
dc_team_id = db.tracker_team.insert_one(dc_team).inserted_id

# Insert team members (many-to-many join table)

# Use integer IDs for team members
team_member_id_counter = 1
for tid, uids in zip([marvel_team['id'], dc_team['id']], [marvel_user_ids, dc_user_ids]):
    for uid in uids:
        db.tracker_team_members.insert_one({'id': team_member_id_counter, 'team_id': tid, 'user_id': uid})
        team_member_id_counter += 1

# Insert activities

# Assign unique integer IDs for activities
activity_id_counter = 1
for uid in marvel_user_ids + dc_user_ids:
    db.tracker_activity.insert_one({
        'id': activity_id_counter,
        'user_id': uid,
        'type': 'run',
        'duration_minutes': 30,
        'distance_km': 5,
        'calories_burned': 300,
        'timestamp': datetime.utcnow(),
    })
    activity_id_counter += 1
    db.tracker_activity.insert_one({
        'id': activity_id_counter,
        'user_id': uid,
        'type': 'cycle',
        'duration_minutes': 60,
        'distance_km': 20,
        'calories_burned': 600,
        'timestamp': datetime.utcnow(),
    })
    activity_id_counter += 1

# Insert workout suggestions

# Assign unique integer IDs for workout suggestions
ws1 = {
    'id': 1,
    'name': 'Morning Run',
    'description': 'Easy 5km run',
    'difficulty': 'easy',
    'target_duration_minutes': 30,
    'target_distance_km': 5,
    'created_by_id': marvel_user_ids[0],
    'created_at': datetime.utcnow(),
}
ws2 = {
    'id': 2,
    'name': 'Hero Cycle',
    'description': 'Challenging 20km cycle',
    'difficulty': 'hard',
    'target_duration_minutes': 60,
    'target_distance_km': 20,
    'created_by_id': dc_user_ids[0],
    'created_at': datetime.utcnow(),
}
db.tracker_workoutsuggestion.insert_many([ws1, ws2])

# Ensure unique index on email
try:
    db.auth_user.create_index('email', unique=True)
except Exception as e:
    print('Index creation error:', e)

print('octofit_db populated with test data!')
