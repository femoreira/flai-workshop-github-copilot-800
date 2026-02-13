from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from datetime import datetime
from .models import Team, User, Activity, Leaderboard, Workout


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            _id='test_team',
            name='Test Team',
            description='Test Description',
            created_at=datetime.now(),
            member_count=0
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team._id, 'test_team')
    
    def test_team_str_method(self):
        """Test the string representation of a team"""
        self.assertEqual(str(self.team), 'Test Team')


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='hashed_password',
            team_id='test_team',
            role='member',
            total_points=100,
            created_at=datetime.now()
        )
    
    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
    
    def test_user_str_method(self):
        """Test the string representation of a user"""
        self.assertEqual(str(self.user), 'Test User')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id='1',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories_burned=300,
            points_earned=50,
            date=datetime.now(),
            notes='Morning run'
        )
    
    def test_activity_creation(self):
        """Test that an activity can be created"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            _id='api_test_team',
            name='API Test Team',
            description='Test Description',
            created_at=datetime.now(),
            member_count=0
        )
    
    def test_get_teams_list(self):
        """Test retrieving the list of teams"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_team_detail(self):
        """Test retrieving a single team"""
        url = reverse('team-detail', args=[self.team._id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Team')


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='API Test User',
            email='apitest@example.com',
            password='hashed_password',
            team_id='test_team',
            role='member',
            total_points=100,
            created_at=datetime.now()
        )
    
    def test_get_users_list(self):
        """Test retrieving the list of users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.activity = Activity.objects.create(
            user_id='1',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories_burned=300,
            points_earned=50,
            date=datetime.now(),
            notes='Test run'
        )
    
    def test_get_activities_list(self):
        """Test retrieving the list of activities"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.leaderboard_entry = Leaderboard.objects.create(
            user_id='1',
            user_name='Test User',
            team_id='test_team',
            total_points=500,
            activities_count=10,
            rank=1,
            last_updated=datetime.now()
        )
    
    def test_get_leaderboard_list(self):
        """Test retrieving the leaderboard"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='Test description',
            duration=45,
            difficulty='intermediate',
            category='strength',
            created_at=datetime.now()
        )
    
    def test_get_workouts_list(self):
        """Test retrieving the list of workouts"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRootTest(APITestCase):
    """Test cases for API root endpoint"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_api_root_accessible(self):
        """Test that the API root is accessible"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('teams', response.data)
        self.assertIn('users', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
