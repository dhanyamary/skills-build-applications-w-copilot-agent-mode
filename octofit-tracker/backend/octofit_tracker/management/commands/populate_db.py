from django.core.management.base import BaseCommand
from django.db import connection
from djongo import models

# Sample superhero and team data
SUPERHEROES = [
    {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
    {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
    {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
    {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
    {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'DC'},
    {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
]
TEAMS = [
    {'name': 'Marvel', 'members': ['Iron Man', 'Captain America', 'Spider-Man']},
    {'name': 'DC', 'members': ['Batman', 'Superman', 'Wonder Woman']},
]
ACTIVITIES = [
    {'user': 'Iron Man', 'activity': 'Running', 'duration': 30},
    {'user': 'Batman', 'activity': 'Cycling', 'duration': 45},
    {'user': 'Superman', 'activity': 'Swimming', 'duration': 60},
]
LEADERBOARD = [
    {'user': 'Superman', 'score': 100},
    {'user': 'Iron Man', 'score': 90},
    {'user': 'Batman', 'score': 80},
]
WORKOUTS = [
    {'name': 'Morning Cardio', 'suggestion': 'Run 5km'},
    {'name': 'Strength Training', 'suggestion': 'Pushups and squats'},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        db = connection.cursor().db_conn.client['octofit_db']
        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db.drop_collection(col)
        # Insert test data
        db.users.insert_many(SUPERHEROES)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)
        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
