from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    # Get user statistics
    routes = Route.objects.filter(user=request.user)
    total_routes = routes.count()
    total_distance = sum(route.distance for route in routes)
    fuel_saved = sum(route.fuel_consumption for route in routes) * 0.15  # Assuming 15% savings
    co2_reduced = fuel_saved * 2.31  # Average CO2 reduction
    
    context = {
        'form': form,
        'total_routes': total_routes,
        'total_distance': f"{total_distance:.1f}",
        'fuel_saved': f"{fuel_saved:.1f}",
        'co2_reduced': f"{co2_reduced:.1f}"
    }
    
    return render(request, 'sdg9/profile.html', context)