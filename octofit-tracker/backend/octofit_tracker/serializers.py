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
        fields = ['id', 'name', 'email', 'password', 'team_id', 'role', 'total_points', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'distance', 
                  'calories_burned', 'points_earned', 'date', 'notes']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_name', 'team_id', 'total_points', 
                  'activities_count', 'rank', 'last_updated']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'duration', 'difficulty', 
                  'exercises', 'category', 'created_at']
