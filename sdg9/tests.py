from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Route, WeatherImpact, TrafficImpact
from .api import WeatherService, RouteService
from unittest.mock import patch
import json

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()

    def test_profile_creation(self):
        """Test that a profile is automatically created for new users"""
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertEqual(self.user.userprofile.vehicle_type, 'four_wheeler')

    def test_profile_update(self):
        """Test profile update functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile'), {
            'vehicle_type': 'two_wheeler',
            'vehicle_model': 'Test Model',
            'fuel_type': 'petrol',
            'average_mileage': 25.0
        })
        self.assertEqual(response.status_code, 302)
        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.vehicle_type, 'two_wheeler')

class RouteCalculationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    @patch('sdg9.api.RouteService.get_routes')
    @patch('sdg9.api.WeatherService.get_weather_data')
    def test_route_calculation(self, mock_weather, mock_routes):
        """Test route calculation with mocked API responses"""
        # Mock API responses
        mock_routes.return_value = [{
            'legs': [{
                'distance': {'value': 10000},
                'duration': {'value': 1200},
                'end_location': {'lat': 0, 'lng': 0}
            }],
            'overview_polyline': {'points': 'test_polyline'}
        }]
        
        mock_weather.return_value = {
            'main': {
                'temp': 20,
                'humidity': 50
            }
        }

        response = self.client.post(
            reverse('calculate_route'),
            json.dumps({
                'origin': 'Test Origin',
                'destination': 'Test Destination'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('routes', data)

class WeatherImpactTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.route = Route.objects.create(
            user=self.user,
            source='Test Origin',
            destination='Test Destination',
            distance=10.0,
            duration=30,
            fuel_consumption=1.0,
            carbon_emissions=2.31,
            weather_condition='Clear'
        )

    def test_weather_impact_calculation(self):
        """Test weather impact calculations"""
        weather_impact = WeatherImpact.objects.create(
            route=self.route,
            temperature=25.0,
            humidity=60.0,
            wind_speed=10.0,
            precipitation=0.0,
            weather_condition='Clear',
            impact_percentage=1.0
        )
        self.assertEqual(weather_impact.impact_percentage, 1.0)

class APIEndpointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_weather_conditions_endpoint(self):
        """Test weather conditions API endpoint"""
        response = self.client.get(
            reverse('weather_conditions'),
            {'lat': '0', 'lng': '0'}
        )
        self.assertEqual(response.status_code, 200)

    def test_traffic_conditions_endpoint(self):
        """Test traffic conditions API endpoint"""
        response = self.client.get(
            reverse('traffic_conditions'),
            {'origin': 'Test Origin', 'destination': 'Test Destination'}
        )
        self.assertEqual(response.status_code, 200)