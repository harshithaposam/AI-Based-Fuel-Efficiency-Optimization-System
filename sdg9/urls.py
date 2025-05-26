from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('route-optimization/', views.route_optimization, name='route_optimization'),
    path('factor-analysis/', views.factor_analysis, name='factor_analysis'),
    path('insights/', views.insights, name='insights'),
    path('profile/', views.profile, name='profile'),
    path('api/calculate-route/', views.calculate_route, name='calculate_route'),
    path('calculate_route/', views.calculate_route, name='calculate_route'),
    path('award_credits/', views.award_credits, name='award_credits'),
]