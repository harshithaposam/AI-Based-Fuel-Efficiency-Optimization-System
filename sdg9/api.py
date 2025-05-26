from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
import json
from .models import Route, WeatherImpact, TrafficImpact
import googlemaps
from datetime import datetime

class WeatherService:
    @staticmethod
    def get_weather_data(lat, lng):
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

class RouteService:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    def get_routes(self, origin, destination):
        routes = self.gmaps.directions(
            origin,
            destination,
            alternatives=True,
            departure_time=datetime.now()
        )
        return routes
    
    def get_elevation(self, path):
        elevation_data = self.gmaps.elevation_along_path(path, samples=10)
        return elevation_data

@login_required
def calculate_route(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        origin = data.get('origin')
        destination = data.get('destination')
        
        route_service = RouteService()
        routes = route_service.get_routes(origin, destination)
        
        processed_routes = []
        for route in routes:
            # Get weather data for destination
            dest_lat = route['legs'][0]['end_location']['lat']
            dest_lng = route['legs'][0]['end_location']['lng']
            weather_data = WeatherService.get_weather_data(dest_lat, dest_lng)
            
            # Process route data
            route_info = process_route(route, weather_data, request.user)
            processed_routes.append(route_info)
        
        return JsonResponse({'routes': processed_routes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_weather_conditions(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    
    if lat and lng:
        weather_data = WeatherService.get_weather_data(lat, lng)
        if weather_data:
            return JsonResponse(weather_data)
    
    return JsonResponse({'error': 'Unable to fetch weather data'}, status=400)

@login_required
def get_traffic_conditions(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    
    if origin and destination:
        route_service = RouteService()
        routes = route_service.get_routes(origin, destination)
        
        if routes:
            traffic_data = {
                'congestion_level': calculate_congestion_level(routes[0]),
                'delay_minutes': calculate_delay(routes[0]),
                'alternative_routes': len(routes)
            }
            return JsonResponse(traffic_data)
    
    return JsonResponse({'error': 'Unable to fetch traffic data'}, status=400)

def process_route(route, weather_data, user):
    distance = route['legs'][0]['distance']['value'] / 1000  # Convert to km
    duration = route['legs'][0]['duration']['value'] / 60    # Convert to minutes
    
    # Calculate base fuel consumption
    vehicle_profile = user.userprofile
    base_consumption = calculate_base_consumption(distance, vehicle_profile)
    
    # Apply weather impact
    weather_impact = calculate_weather_impact(weather_data)
    
    # Apply traffic impact
    traffic_impact = calculate_traffic_impact(route)
    
    # Calculate final fuel consumption
    fuel_consumption = base_consumption * weather_impact * traffic_impact
    
    # Calculate carbon emissions
    emissions = calculate_carbon_emissions(fuel_consumption, vehicle_profile.fuel_type)
    
    return {
        'distance': f"{distance:.1f} km",
        'duration': f"{duration:.0f} min",
        'fuel_consumption': f"{fuel_consumption:.2f}",
        'emissions': f"{emissions:.2f}",
        'weather_impact': f"{(weather_impact - 1) * 100:+.1f}%",
        'traffic_impact': f"{(traffic_impact - 1) * 100:+.1f}%",
        'polyline': route['overview_polyline']['points']
    }

def calculate_base_consumption(distance, profile):
    # Basic consumption calculation based on vehicle type and average mileage
    if profile.vehicle_type == 'two_wheeler':
        return distance * 0.03  # Example: 3L/100km
    return distance * 0.07      # Example: 7L/100km

def calculate_weather_impact(weather_data):
    if not weather_data:
        return 1.0
    
    impact = 1.0
    temp = weather_data['main']['temp']
    
    # Temperature impact
    if temp < 10 or temp > 30:
        impact *= 1.1
    
    # Rain impact
    if 'rain' in weather_data:
        impact *= 1.15
    
    return impact

def calculate_traffic_impact(route):
    if 'duration_in_traffic' in route['legs'][0]:
        normal_duration = route['legs'][0]['duration']['value']
        traffic_duration = route['legs'][0]['duration_in_traffic']['value']
        
        ratio = traffic_duration / normal_duration
        if ratio > 2:
            return 1.4    # Severe traffic
        elif ratio > 1.5:
            return 1.25   # Heavy traffic
        elif ratio > 1.2:
            return 1.1    # Moderate traffic
    
    return 1.0

def calculate_carbon_emissions(fuel_consumption, fuel_type):
    # CO2 emissions in kg per liter of fuel
    emissions_factor = {
        'petrol': 2.31,
        'diesel': 2.68,
        'electric': 0,
        'hybrid': 1.7
    }
    return fuel_consumption * emissions_factor.get(fuel_type, 2.31)