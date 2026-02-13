from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from bson import ObjectId
from .models import Team, User, Activity, Leaderboard, Workout
from .serializers import (
    TeamSerializer, UserSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams.
    Provides CRUD operations for Team model.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = '_id'

    def get_object(self):
        """Override to handle ObjectId conversion for MongoDB"""
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # Find object by comparing string representation of _id
        for obj in queryset:
            if str(obj._id) == lookup_value:
                self.check_object_permissions(self.request, obj)
                return obj
        
        from rest_framework.exceptions import NotFound
        raise NotFound('No Team matches the given query.')

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        users = User.objects.filter(team_id=team._id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    Provides CRUD operations for User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = '_id'

    def get_object(self):
        """Override to handle ObjectId conversion for MongoDB"""
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # Find object by comparing string representation of _id
        for obj in queryset:
            if str(obj._id) == lookup_value:
                self.check_object_permissions(self.request, obj)
                return obj
        
        from rest_framework.exceptions import NotFound
        raise NotFound('No User matches the given query.')

    def update(self, request, *args, **kwargs):
        """Override update to use PyMongo directly for MongoDB"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Update using PyMongo directly
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']
        
        update_data = {}
        for key, value in serializer.validated_data.items():
            if  key != '_id':  # Don't update _id
                update_data[key] = value
        
        if update_data:
            result = db.users.update_one(
                {'_id': ObjectId(str(instance._id))},
                {'$set': update_data}
            )
        
        # Fetch updated user
        updated_user = self.get_object()
        serializer = self.get_serializer(updated_user)
        
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=str(user.id))
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get all users filtered by team"""
        team_id = request.query_params.get('team_id', None)
        if team_id:
            users = User.objects.filter(team_id=team_id)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'team_id parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities.
    Provides CRUD operations for Activity model.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    lookup_field = '_id'

    def get_object(self):
        """Override to handle ObjectId conversion for MongoDB"""
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # Find object by comparing string representation of _id
        for obj in queryset:
            if str(obj._id) == lookup_value:
                self.check_object_permissions(self.request, obj)
                return obj
        
        from rest_framework.exceptions import NotFound
        raise NotFound('No Activity matches the given query.')

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get all activities filtered by user"""
        user_id = request.query_params.get('user_id', None)
        if user_id:
            activities = Activity.objects.filter(user_id=user_id)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'user_id parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get all activities filtered by activity type"""
        activity_type = request.query_params.get('type', None)
        if activity_type:
            activities = Activity.objects.filter(activity_type=activity_type)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'type parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leaderboard.
    Provides CRUD operations for Leaderboard model.
    """
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer
    lookup_field = '_id'

    def get_object(self):
        """Override to handle ObjectId conversion for MongoDB"""
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # Find object by comparing string representation of _id
        for obj in queryset:
            if str(obj._id) == lookup_value:
                self.check_object_permissions(self.request, obj)
                return obj
        
        from rest_framework.exceptions import NotFound
        raise NotFound('No Leaderboard matches the given query.')

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard filtered by team"""
        team_id = request.query_params.get('team_id', None)
        if team_id:
            leaderboard = Leaderboard.objects.filter(team_id=team_id).order_by('rank')
            serializer = self.get_serializer(leaderboard, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'team_id parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top N users from leaderboard"""
        limit = int(request.query_params.get('limit', 10))
        leaderboard = Leaderboard.objects.all().order_by('rank')[:limit]
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workouts.
    Provides CRUD operations for Workout model.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    lookup_field = '_id'

    def get_object(self):
        """Override to handle ObjectId conversion for MongoDB"""
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # Find object by comparing string representation of _id
        for obj in queryset:
            if str(obj._id) == lookup_value:
                self.check_object_permissions(self.request, obj)
                return obj
        
        from rest_framework.exceptions import NotFound
        raise NotFound('No Workout matches the given query.')

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts filtered by difficulty"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'difficulty parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get workouts filtered by category"""
        category = request.query_params.get('category', None)
        if category:
            workouts = Workout.objects.filter(category=category)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'category parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
