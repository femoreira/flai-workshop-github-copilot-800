from django.core.management.base import BaseCommand
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write('Clearing existing data...')
        
        # Clear existing collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # Create unique index on email field for users
        self.stdout.write('Creating unique index on user email...')
        db.users.create_index([("email", ASCENDING)], unique=True)
        self.stdout.write(self.style.SUCCESS('Index created.'))

        # Team Marvel and Team DC
        teams_data = [
            {
                '_id': 'team_marvel',
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'created_at': datetime.now(),
                'member_count': 0
            },
            {
                '_id': 'team_dc',
                'name': 'Team DC',
                'description': 'Justice League Champions',
                'created_at': datetime.now(),
                'member_count': 0
            }
        ]

        # Insert teams
        self.stdout.write('Inserting teams...')
        db.teams.insert_many(teams_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(teams_data)} teams.'))

        # Marvel and DC superheroes
        users_data = [
            # Team Marvel
            {
                'name': 'Tony Stark',
                'email': 'ironman@marvel.com',
                'password': 'hashed_password_1',
                'team_id': 'team_marvel',
                'role': 'leader',
                'total_points': 2500,
                'created_at': datetime.now()
            },
            {
                'name': 'Steve Rogers',
                'email': 'captainamerica@marvel.com',
                'password': 'hashed_password_2',
                'team_id': 'team_marvel',
                'role': 'member',
                'total_points': 2300,
                'created_at': datetime.now()
            },
            {
                'name': 'Natasha Romanoff',
                'email': 'blackwidow@marvel.com',
                'password': 'hashed_password_3',
                'team_id': 'team_marvel',
                'role': 'member',
                'total_points': 2200,
                'created_at': datetime.now()
            },
            {
                'name': 'Bruce Banner',
                'email': 'hulk@marvel.com',
                'password': 'hashed_password_4',
                'team_id': 'team_marvel',
                'role': 'member',
                'total_points': 2100,
                'created_at': datetime.now()
            },
            {
                'name': 'Thor Odinson',
                'email': 'thor@marvel.com',
                'password': 'hashed_password_5',
                'team_id': 'team_marvel',
                'role': 'member',
                'total_points': 2400,
                'created_at': datetime.now()
            },
            # Team DC
            {
                'name': 'Clark Kent',
                'email': 'superman@dc.com',
                'password': 'hashed_password_6',
                'team_id': 'team_dc',
                'role': 'leader',
                'total_points': 2600,
                'created_at': datetime.now()
            },
            {
                'name': 'Bruce Wayne',
                'email': 'batman@dc.com',
                'password': 'hashed_password_7',
                'team_id': 'team_dc',
                'role': 'member',
                'total_points': 2450,
                'created_at': datetime.now()
            },
            {
                'name': 'Diana Prince',
                'email': 'wonderwoman@dc.com',
                'password': 'hashed_password_8',
                'team_id': 'team_dc',
                'role': 'member',
                'total_points': 2350,
                'created_at': datetime.now()
            },
            {
                'name': 'Barry Allen',
                'email': 'flash@dc.com',
                'password': 'hashed_password_9',
                'team_id': 'team_dc',
                'role': 'member',
                'total_points': 2250,
                'created_at': datetime.now()
            },
            {
                'name': 'Arthur Curry',
                'email': 'aquaman@dc.com',
                'password': 'hashed_password_10',
                'team_id': 'team_dc',
                'role': 'member',
                'total_points': 2150,
                'created_at': datetime.now()
            }
        ]

        # Insert users
        self.stdout.write('Inserting users...')
        result = db.users.insert_many(users_data)
        user_ids = result.inserted_ids
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(users_data)} users.'))

        # Update team member counts
        db.teams.update_one({'_id': 'team_marvel'}, {'$set': {'member_count': 5}})
        db.teams.update_one({'_id': 'team_dc'}, {'$set': {'member_count': 5}})

        # Activity types
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'CrossFit']
        
        # Generate activities for each user
        self.stdout.write('Inserting activities...')
        activities_data = []
        for i, user_id in enumerate(user_ids):
            for _ in range(random.randint(5, 10)):
                activity_type = random.choice(activity_types)
                duration = random.randint(30, 180)  # 30 to 180 minutes
                distance = round(random.uniform(1, 25), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else 0
                calories = duration * random.randint(5, 15)
                points = duration * 2 + int(distance * 10)
                
                activities_data.append({
                    'user_id': user_id,
                    'activity_type': activity_type,
                    'duration': duration,  # minutes
                    'distance': distance,  # km
                    'calories_burned': calories,
                    'points_earned': points,
                    'date': datetime.now() - timedelta(days=random.randint(0, 30)),
                    'notes': f'{activity_type} session with {users_data[i]["name"]}'
                })

        db.activities.insert_many(activities_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(activities_data)} activities.'))

        # Generate leaderboard entries
        self.stdout.write('Inserting leaderboard entries...')
        leaderboard_data = []
        for i, user in enumerate(users_data):
            leaderboard_data.append({
                'user_id': user_ids[i],
                'user_name': user['name'],
                'team_id': user['team_id'],
                'total_points': user['total_points'],
                'activities_count': random.randint(5, 10),
                'rank': 0,  # Will be calculated
                'last_updated': datetime.now()
            })

        # Sort by points and assign ranks
        leaderboard_data.sort(key=lambda x: x['total_points'], reverse=True)
        for rank, entry in enumerate(leaderboard_data, start=1):
            entry['rank'] = rank

        db.leaderboard.insert_many(leaderboard_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(leaderboard_data)} leaderboard entries.'))

        # Generate workout suggestions
        self.stdout.write('Inserting workout suggestions...')
        workouts_data = [
            {
                'name': 'Hero Strength Training',
                'description': 'Build strength like a superhero',
                'duration': 60,
                'difficulty': 'intermediate',
                'exercises': [
                    {'name': 'Push-ups', 'sets': 3, 'reps': 15},
                    {'name': 'Pull-ups', 'sets': 3, 'reps': 10},
                    {'name': 'Squats', 'sets': 3, 'reps': 20},
                    {'name': 'Plank', 'sets': 3, 'duration': '60 seconds'}
                ],
                'category': 'strength',
                'created_at': datetime.now()
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'Run as fast as The Flash',
                'duration': 45,
                'difficulty': 'advanced',
                'exercises': [
                    {'name': 'Sprint Intervals', 'sets': 5, 'duration': '2 minutes'},
                    {'name': 'Burpees', 'sets': 3, 'reps': 15},
                    {'name': 'Jump Rope', 'sets': 3, 'duration': '3 minutes'},
                    {'name': 'Mountain Climbers', 'sets': 3, 'reps': 30}
                ],
                'category': 'cardio',
                'created_at': datetime.now()
            },
            {
                'name': 'Warrior Flexibility',
                'description': 'Flexibility training fit for Wonder Woman',
                'duration': 30,
                'difficulty': 'beginner',
                'exercises': [
                    {'name': 'Yoga Flow', 'sets': 1, 'duration': '15 minutes'},
                    {'name': 'Static Stretches', 'sets': 1, 'duration': '10 minutes'},
                    {'name': 'Deep Breathing', 'sets': 1, 'duration': '5 minutes'}
                ],
                'category': 'flexibility',
                'created_at': datetime.now()
            },
            {
                'name': 'Asgardian Power Workout',
                'description': 'Train like Thor with hammer swings',
                'duration': 90,
                'difficulty': 'advanced',
                'exercises': [
                    {'name': 'Deadlifts', 'sets': 4, 'reps': 8},
                    {'name': 'Overhead Press', 'sets': 4, 'reps': 10},
                    {'name': 'Battle Ropes', 'sets': 3, 'duration': '2 minutes'},
                    {'name': 'Farmer\'s Walk', 'sets': 3, 'distance': '50 meters'}
                ],
                'category': 'strength',
                'created_at': datetime.now()
            },
            {
                'name': 'Detective Core Training',
                'description': 'Batman\'s core workout routine',
                'duration': 40,
                'difficulty': 'intermediate',
                'exercises': [
                    {'name': 'Hanging Leg Raises', 'sets': 3, 'reps': 12},
                    {'name': 'Russian Twists', 'sets': 3, 'reps': 30},
                    {'name': 'Ab Wheel Rollouts', 'sets': 3, 'reps': 10},
                    {'name': 'Side Plank', 'sets': 3, 'duration': '45 seconds'}
                ],
                'category': 'core',
                'created_at': datetime.now()
            }
        ]

        db.workouts.insert_many(workouts_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workouts_data)} workout suggestions.'))

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write('='*50)
        self.stdout.write(f'Teams: {db.teams.count_documents({})}')
        self.stdout.write(f'Users: {db.users.count_documents({})}')
        self.stdout.write(f'Activities: {db.activities.count_documents({})}')
        self.stdout.write(f'Leaderboard entries: {db.leaderboard.count_documents({})}')
        self.stdout.write(f'Workout suggestions: {db.workouts.count_documents({})}')
        self.stdout.write('='*50 + '\n')

        client.close()
