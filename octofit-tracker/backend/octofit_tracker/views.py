from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
