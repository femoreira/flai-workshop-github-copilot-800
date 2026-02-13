from django.contrib import admin
from .models import Team, User, Activity, Leaderboard, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['_id', 'name', 'member_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['_id', 'name', 'email', 'team_id', 'role', 'total_points', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['role', 'team_id', 'created_at']
    ordering = ['-total_points']
    readonly_fields = ['created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['_id', 'user_id', 'activity_type', 'duration', 'distance', 
                    'calories_burned', 'points_earned', 'date']
    search_fields = ['user_id', 'activity_type', 'notes']
    list_filter = ['activity_type', 'date']
    ordering = ['-date']
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['rank', 'user_name', 'team_id', 'total_points', 
                    'activities_count', 'last_updated']
    search_fields = ['user_name', 'user_id']
    list_filter = ['team_id', 'last_updated']
    ordering = ['rank']
    readonly_fields = ['last_updated']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['_id', 'name', 'category', 'difficulty', 'duration', 'created_at']
    search_fields = ['name', 'description', 'category']
    list_filter = ['difficulty', 'category', 'created_at']
    ordering = ['name']
    readonly_fields = ['created_at']
