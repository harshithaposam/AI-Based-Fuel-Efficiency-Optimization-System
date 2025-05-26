document.addEventListener('DOMContentLoaded', function() {
    // Update weather-based tips based on current weather
    updateWeatherTips();
    
    // Update traffic-based tips
    updateTrafficTips();
    
    // Refresh data every 5 minutes
    setInterval(function() {
        updateWeatherTips();
        updateTrafficTips();
    }, 300000);
});

function updateWeatherTips() {
    // Get current weather data and update tips
    fetch('/api/current-weather/')
        .then(response => response.json())
        .then(data => {
            const tipsList = document.querySelector('#weatherTips ul');
            tipsList.innerHTML = '';
            
            const tips = generateWeatherTips(data);
            tips.forEach(tip => {
                const li = document.createElement('li');
                li.textContent = tip;
                tipsList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching weather data:', error));
}

function updateTrafficTips() {
    // Get current traffic data and update tips
    fetch('/api/traffic-conditions/')
        .then(response => response.json())
        .then(data => {
            const tipsList = document.querySelector('#trafficTips ul');
            tipsList.innerHTML = '';
            
            const tips = generateTrafficTips(data);
            tips.forEach(tip => {
                const li = document.createElement('li');
                li.textContent = tip;
                tipsList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching traffic data:', error));
}

function generateWeatherTips(weatherData) {
    const tips = [];
    
    if (weatherData.temperature > 30) {
        tips.push('High temperature: Use AC moderately to save fuel');
        tips.push('Consider traveling during cooler hours');
    }
    
    if (weatherData.rain) {
        tips.push('Rainy conditions: Maintain steady speed for better efficiency');
        tips.push('Ensure proper tire pressure for wet conditions');
    }
    
    if (weatherData.wind > 20) {
        tips.push('Strong winds: Reduce speed to improve fuel efficiency');
    }
    
    return tips;
}

function generateTrafficTips(trafficData) {
    const tips = [];
    
    if (trafficData.congestion === 'heavy') {
        tips.push('Heavy traffic: Consider alternative routes');
        tips.push('Avoid rapid acceleration and braking');
    }
    
    if (trafficData.peakHours) {
        tips.push('Peak hours: Plan your journey during off-peak times');
    }
    
    return tips;
}