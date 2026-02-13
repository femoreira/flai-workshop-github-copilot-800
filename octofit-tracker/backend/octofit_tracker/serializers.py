from rest_framework import serializers
from .models import Team, User, Activity, Leaderboard, Workout


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at', 'member_count']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'password', 'team_id', 'role', 'total_points', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['_id', 'user_id', 'user_name', 'activity_type', 'duration', 'distance', 
                  'calories_burned', 'points_earned', 'date', 'notes']
    
    def get_user_name(self, obj):
        """Get user name from user_id using MongoDB directly"""
        try:
            from pymongo import MongoClient
            client = MongoClient('mongodb://localhost:27017/')
            db = client['octofit_db']
            user = db.users.find_one({'_id': obj.user_id})
            if user:
                return user.get('name', 'Unknown User')
            return 'Unknown User'
        except Exception as e:
            return 'Unknown User'


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user_id', 'user_name', 'team_id', 'total_points', 
                  'activities_count', 'rank', 'last_updated']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    exercises = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'duration', 'difficulty', 
                  'exercises', 'category', 'created_at']
    
    def get_exercises(self, obj):
        """Handle exercises field which comes from MongoDB as a list"""
        try:
            # If exercises is already a list, return it as-is
            if isinstance(obj.exercises, list):
                return obj.exercises
            # If it's None or empty, return empty list
            elif obj.exercises is None or obj.exercises == '':
                return []
            # If it's a string, try to parse it as JSON
            else:
                import json
                return json.loads(obj.exercises)
        except:
            return []
