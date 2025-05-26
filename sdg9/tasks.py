from celery import shared_task
from django.core.cache import cache
from .models import Route, WeatherImpact, TrafficImpact
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('sdg9')

@shared_task
def update_route_statistics():
    """
    Update route statistics and cache the results
    """
    try:
        # Get routes from the last 24 hours
        recent_routes = Route.objects.filter(
            created_at__gte=datetime.now() - timedelta(days=1)
        )

        stats = {
            'total_routes': recent_routes.count(),
            'total_distance': sum(route.distance for route in recent_routes),
            'total_fuel': sum(route.fuel_consumption for route in recent_routes),
            'total_emissions': sum(route.carbon_emissions for route in recent_routes),
        }

        # Cache the results
        cache.set('route_statistics', stats, timeout=3600)  # 1 hour cache
        return stats

    except Exception as e:
        logger.error(f"Error updating route statistics: {e}")
        return None

@shared_task
def analyze_weather_impacts():
    """
    Analyze weather impacts on fuel efficiency
    """
    try:
        weather_impacts = WeatherImpact.objects.all()
        analysis = {
            'temperature_impact': {},
            'humidity_impact': {},
            'precipitation_impact': {}
        }

        for impact in weather_impacts:
            temp_range = f"{int(impact.temperature//5)*5}-{int(impact.temperature//5)*5+5}"
            analysis['temperature_impact'][temp_range] = analysis['temperature_impact'].get(temp_range, 0) + 1

        cache.set('weather_impact_analysis', analysis, timeout=3600)
        return analysis

    except Exception as e:
        logger.error(f"Error analyzing weather impacts: {e}")
        return None

@shared_task
def analyze_traffic_patterns():
    """
    Analyze traffic patterns and their impact on fuel efficiency
    """
    try:
        traffic_impacts = TrafficImpact.objects.all()
        analysis = {
            'congestion_levels': {},
            'average_delays': {},
            'peak_hours': {}
        }

        for impact in traffic_impacts:
            hour = impact.route.created_at.hour
            analysis['peak_hours'][hour] = analysis['peak_hours'].get(hour, 0) + 1

        cache.set('traffic_pattern_analysis', analysis, timeout=3600)
        return analysis

    except Exception as e:
        logger.error(f"Error analyzing traffic patterns: {e}")
        return None

@shared_task
def calculate_route_recommendations(user_id):
    """
    Calculate personalized route recommendations for a user
    """
    try:
        from .models import UserProfile
        profile = UserProfile.objects.get(user_id=user_id)
        routes = Route.objects.filter(user_id=user_id)

        recommendations = {
            'preferred_times': [],
            'efficient_routes': [],
            'weather_considerations': []
        }

        # Analyze user's route history
        if routes.exists():
            # Find most efficient routes
            efficient_routes = routes.order_by('fuel_consumption')[:3]
            recommendations['efficient_routes'] = list(efficient_routes.values())

            # Analyze timing patterns
            route_times = routes.values_list('created_at', flat=True)
            hour_counts = {}
            for dt in route_times:
                hour_counts[dt.hour] = hour_counts.get(dt.hour, 0) + 1
            
            # Find preferred times
            preferred_times = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            recommendations['preferred_times'] = preferred_times

        cache.set(f'user_recommendations_{user_id}', recommendations, timeout=3600)
        return recommendations

    except Exception as e:
        logger.error(f"Error calculating route recommendations: {e}")
        return None