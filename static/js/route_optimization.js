let map;
let directionsService;
let directionsRenderer;
let markers = [];

function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7,
        center: { lat: 20.5937, lng: 78.9629 } // India center
    });
    
    directionsRenderer.setMap(map);
    
    // Initialize autocomplete
    const originInput = document.getElementById('origin');
    const destinationInput = document.getElementById('destination');
    
    new google.maps.places.Autocomplete(originInput);
    new google.maps.places.Autocomplete(destinationInput);
    
    // Form submission handler
    document.getElementById('routeForm').addEventListener('submit', calculateRoutes);
}

function calculateRoutes(e) {
    e.preventDefault();
    
    const origin = document.getElementById('origin').value;
    const destination = document.getElementById('destination').value;
    
    fetch('/api/calculate-route/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            origin: origin,
            destination: destination
        })
    })
    .then(response => response.json())
    .then(data => displayRoutes(data.routes))
    .catch(error => console.error('Error:', error));
}

function displayRoutes(routes) {
    const routesList = document.getElementById('routesList');
    routesList.innerHTML = '';
    
    routes.forEach((route, index) => {
        const routeDiv = document.createElement('div');
        routeDiv.className = 'route-option';
        routeDiv.innerHTML = `
            <h6>Route ${index + 1}</h6>
            <p>Distance: ${route.distance}</p>
            <p>Duration: ${route.duration}</p>
            <p>Fuel: ${route.fuel_consumption}L</p>
            <p>CO2: ${route.emissions}kg</p>
        `;
        routesList.appendChild(routeDiv);
    });
    
    document.getElementById('routeResults').style.display = 'block';
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize map when the page loads
window.addEventListener('load', initMap);