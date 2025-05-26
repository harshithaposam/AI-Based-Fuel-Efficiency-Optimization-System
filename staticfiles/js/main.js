// Utility functions
const API = {
    async post(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    async get(url, params = {}) {
        try {
            const queryString = new URLSearchParams(params).toString();
            const response = await fetch(`${url}?${queryString}`);
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
};

// Error handling
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('main').prepend(errorDiv);
}

// Loading indicator
const LoadingIndicator = {
    show() {
        const loader = document.createElement('div');
        loader.id = 'loading-indicator';
        loader.className = 'position-fixed top-50 start-50 translate-middle';
        loader.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `;
        document.body.appendChild(loader);
    },

    hide() {
        const loader = document.getElementById('loading-indicator');
        if (loader) loader.remove();
    }
};

// Form validation
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
            
            const feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            feedback.textContent = 'This field is required';
            input.parentNode.appendChild(feedback);
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Route visualization
class RouteVisualizer {
    constructor(mapElement) {
        this.map = new google.maps.Map(mapElement, {
            zoom: 7,
            center: { lat: 20.5937, lng: 78.9629 }
        });
        this.directionsService = new google.maps.DirectionsService();
        this.directionsRenderer = new google.maps.DirectionsRenderer();
        this.directionsRenderer.setMap(this.map);
    }

    async visualizeRoute(origin, destination) {
        try {
            LoadingIndicator.show();
            const result = await this.directionsService.route({
                origin,
                destination,
                travelMode: google.maps.TravelMode.DRIVING
            });
            this.directionsRenderer.setDirections(result);
            return result;
        } catch (error) {
            showError('Error calculating route: ' + error.message);
            throw error;
        } finally {
            LoadingIndicator.hide();
        }
    }

    clearRoute() {
        this.directionsRenderer.setDirections({ routes: [] });
    }
}

// Weather visualization
class WeatherVisualizer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    async showWeather(lat, lng) {
        try {
            LoadingIndicator.show();
            const weather = await API.get('/api/weather-conditions/', { lat, lng });
            this.updateUI(weather);
        } catch (error) {
            showError('Error fetching weather data: ' + error.message);
        } finally {
            LoadingIndicator.hide();
        }
    }

    updateUI(weather) {
        this.container.innerHTML = `
            <div class="weather-info">
                <h4>Weather Conditions</h4>
                <p>Temperature: ${weather.main.temp}°C</p>
                <p>Humidity: ${weather.main.humidity}%</p>
                <p>Conditions: ${weather.weather[0].description}</p>
            </div>
        `;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    });

    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));

    // Initialize route visualization if map element exists
    const mapElement = document.getElementById('map');
    if (mapElement) {
        const routeVisualizer = new RouteVisualizer(mapElement);
        window.routeVisualizer = routeVisualizer;
    }
});