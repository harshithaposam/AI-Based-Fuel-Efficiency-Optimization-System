from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class NotificationManager:
    @staticmethod
    def send_route_summary(user, route):
        """Send route summary email"""
        context = {
            'user': user,
            'route': route,
            'date': timezone.now().strftime('%Y-%m-%d %H:%M')
        }
        
        html_message = render_to_string('emails/route_summary.html', context)
        
        send_mail(
            subject='Your Route Summary',
            message='',
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

    @staticmethod
    def send_weekly_report(user):
        """Send weekly efficiency report"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        
        from sdg9.models import Route
        routes = Route.objects.filter(
            user=user,
            created_at__range=(start_date, end_date)
        )
        
        context = {
            'user': user,
            'routes': routes,
            'total_distance': sum(r.distance for r in routes),
            'total_fuel_saved': sum(r.fuel_consumption for r in routes) * 0.15,
            'total_emissions_saved': sum(r.carbon_emissions for r in routes) * 0.15,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }
        
        html_message = render_to_string('emails/weekly_report.html', context)
        
        send_mail(
            subject='Your Weekly Efficiency Report',
            message='',
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

    @staticmethod
    def send_efficiency_alert(user, route):
        """Send alert when route efficiency is significantly lower"""
        if route.fuel_consumption / route.distance > user.userprofile.average_mileage * 1.2:
            context = {
                'user': user,
                'route': route,
                'date': timezone.now().strftime('%Y-%m-%d %H:%M'),
                'efficiency_difference': (
                    (route.fuel_consumption / route.distance) - 
                    user.userprofile.average_mileage
                ) / user.userprofile.average_mileage * 100
            }
            
            html_message = render_to_string('emails/efficiency_alert.html', context)
            
            send_mail(
                subject='Efficiency Alert',
                message='',
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )