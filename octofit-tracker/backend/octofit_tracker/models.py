from django.db import models
from djongo import models as djongo_models


class Team(models.Model):
    """Team model representing fitness teams"""
    _id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField()
    member_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'teams'
        
    def __str__(self):
        return self.name


class User(models.Model):
    """User model representing team members"""
    _id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    team_id = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model representing workout activities"""
    _id = models.CharField(max_length=100, primary_key=True)
    user_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # minutes
    distance = models.FloatField(default=0)  # km
    calories_burned = models.IntegerField()
    points_earned = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'
        verbose_name_plural = 'Activities'
        
    def __str__(self):
        return f"{self.activity_type} - {self.duration}min"


class Leaderboard(models.Model):
    """Leaderboard model for ranking users"""
    _id = models.CharField(max_length=100, primary_key=True)
    user_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=100)
    total_points = models.IntegerField()
    activities_count = models.IntegerField()
    rank = models.IntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
        
    def __str__(self):
        return f"{self.rank}. {self.user_name} - {self.total_points} pts"


class Workout(models.Model):
    """Workout model representing workout suggestions"""
    _id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField()  # minutes
    difficulty = models.CharField(max_length=50)
    exercises = models.TextField(null=True, blank=True)  # Will be handled by serializer
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'workouts'
        
    def __str__(self):
        return self.name
