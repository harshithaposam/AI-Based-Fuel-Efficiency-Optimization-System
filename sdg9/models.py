from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CarModel(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=20)
    mileage = models.FloatField()
    co2_emissions = models.FloatField()

    def __str__(self):
        return f"{self.brand} {self.model} ({self.fuel_type})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=20, choices=[
        ('two_wheeler', 'Two Wheeler'),
        ('four_wheeler', 'Four Wheeler'),
    ])
    average_mileage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    distance = models.FloatField()
    duration = models.IntegerField()  # in minutes
    fuel_consumption = models.FloatField()
    carbon_emissions = models.FloatField()
    weather_condition = models.CharField(max_length=100)
    traffic_condition = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.source} to {self.destination}"

class WeatherImpact(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    precipitation = models.FloatField()
    weather_condition = models.CharField(max_length=100)
    impact_percentage = models.FloatField()
    
    def __str__(self):
        return f"Weather impact on {self.route}"

class TrafficImpact(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    congestion_level = models.CharField(max_length=20)
    delay_minutes = models.IntegerField()
    impact_percentage = models.FloatField()
    
    def __str__(self):
        return f"Traffic impact on {self.route}"

class UserCredit(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.user.username} - {self.credits} credits"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        UserCredit.objects.create(user=user_profile)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()