from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('vehicle_type', 'vehicle_model', 'fuel_type', 'average_mileage')
        widgets = {
            'average_mileage': forms.NumberInput(attrs={'step': '0.1'})
        }

class RouteForm(forms.Form):
    origin = forms.CharField(max_length=255)
    destination = forms.CharField(max_length=255)
    vehicle_type = forms.ChoiceField(choices=[
        ('two_wheeler', 'Two Wheeler'),
        ('four_wheeler', 'Four Wheeler')
    ])