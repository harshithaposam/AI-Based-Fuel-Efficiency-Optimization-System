import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el.settings')

app = Celery('el')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure Celery Beat schedule
app.conf.beat_schedule = {
    'update-route-statistics': {
        'task': 'sdg9.tasks.update_route_statistics',
        'schedule': 300.0,  # 5 minutes
    },
    'analyze-weather-impacts': {
        'task': 'sdg9.tasks.analyze_weather_impacts',
        'schedule': 3600.0,  # 1 hour
    },
    'analyze-traffic-patterns': {
        'task': 'sdg9.tasks.analyze_traffic_patterns',
        'schedule': 1800.0,  # 30 minutes
    },
}