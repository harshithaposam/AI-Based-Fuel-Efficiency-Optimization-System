from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Route, WeatherImpact, UserProfile, UserCredit
import googlemaps
import requests
from django.conf import settings
import json
from django.http import HttpResponse
from .utils.report_generator import ReportGenerator
from datetime import datetime
from .ant_colony import AntColony
import numpy as np

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def home(request):
    return render(request, 'sdg9/home.html')

@login_required
def route_optimization(request):
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'sdg9/route_optimization.html', context)

@login_required
def factor_analysis(request):
    return render(request, 'sdg9/factor_analysis.html')

@login_required
def insights(request):
    user_routes = Route.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'routes': user_routes
    }
    return render(request, 'sdg9/insights.html', context)

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_profile.vehicle_type = request.POST.get('vehicle_type')
        user_profile.save()
        return redirect('profile')
    return render(request, 'sdg9/profile.html', {'profile': user_profile})

def get_lat_lng_for_city(city_name):
    geocode_result = gmaps.geocode(city_name)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return lat, lng
    return None, None

@login_required
def calculate_route(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        origin = data.get('origin')
        destination = data.get('destination')

        place_names = ["Source", "Destination"]
        distances = np.array([
            [0, 10000],
            [10000, 0]
        ])

        ant_colony = AntColony(distances, num_ants=10, num_iterations=100, decay=0.1)
        start = place_names.index(origin)
        end = place_names.index(destination)
        shortest_routes = ant_colony.run(start=start, end=end)

        if isinstance(shortest_routes, str):
            return JsonResponse({'error': shortest_routes}, status=400)

        processed_routes = []
        min_fuel_consumption = float('inf')
        best_route = None

        for route, length in shortest_routes:
            polyline_points = []
            for city in route:
                lat, lng = get_lat_lng_for_city(place_names[city])
                if lat is not None and lng is not None:
                    polyline_points.append({'lat': lat, 'lng': lng})

            fuel_consumption = calculate_fuel_consumption(length, None)
            if fuel_consumption < min_fuel_consumption:
                min_fuel_consumption = fuel_consumption
                best_route = route

            processed_routes.append({
                'route': [place_names[city] for city in route],
                'distance': length,
                'fuel_consumption': fuel_consumption,
                'polyline': polyline_points
            })

        return JsonResponse({'routes': processed_routes, 'best_route': best_route})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def award_credits(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_route_index = data.get('selected_route_index')
            routes = data.get('routes')

            if selected_route_index is None or routes is None:
                return JsonResponse({'error': 'Invalid data'}, status=400)

            user_profile = UserProfile.objects.get(user=request.user)
            user_credit, created = UserCredit.objects.get_or_create(user=user_profile)
            user_credit.credits += 20
            user_credit.save()

            return JsonResponse({'message': 'Credits awarded', 'credits': user_credit.credits})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_weather_data(location):
    geocode_result = gmaps.geocode(location)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(weather_url)
        if response.status_code == 200:
            return response.json()
    return None

def process_routes(routes, weather):
    processed_routes = []
    for route in routes:
        route_info = {
            'distance': route['legs'][0]['distance']['text'],
            'duration': route['legs'][0]['duration']['text'],
            'steps': route['legs'][0]['steps'],
            'polyline': route['overview_polyline']['points'],
        }
        distance_km = route['legs'][0]['distance']['value'] / 1000
        fuel_consumption = calculate_fuel_consumption(distance_km, weather)
        emissions = calculate_emissions(fuel_consumption)
        route_info.update({
            'fuel_consumption': round(fuel_consumption, 2),
            'emissions': round(emissions, 2),
        })
        processed_routes.append(route_info)
    return processed_routes

def calculate_fuel_consumption(distance, weather):
    base_consumption = distance * 0.07
    if weather:
        temp = weather['main']['temp']
        humidity = weather['main']['humidity']
        if temp < 10 or temp > 30:
            base_consumption *= 1.1
        if humidity > 80:
            base_consumption *= 1.05
    return base_consumption

def calculate_emissions(fuel_consumption):
    return fuel_consumption * 2.31

@login_required
def export_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    report_type = request.GET.get('type', 'pdf')
    
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except (ValueError, TypeError):
        return HttpResponse('Invalid date format', status=400)
    
    generator = ReportGenerator(request.user)
    
    if report_type == 'pdf':
        file_path = generator.generate_pdf_report(start_date, end_date)
        content_type = 'application/pdf'
    else:
        file_path = generator.generate_excel_report(start_date, end_date)
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    with default_storage.open(file_path) as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'
        return response