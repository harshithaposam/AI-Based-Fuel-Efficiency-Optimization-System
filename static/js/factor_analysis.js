document.addEventListener('DOMContentLoaded', function() {
    // Weather Impact Chart
    const weatherCtx = document.getElementById('weatherChart').getContext('2d');
    new Chart(weatherCtx, {
        type: 'line',
        data: {
            labels: ['0°C', '10°C', '20°C', '30°C', '40°C'],
            datasets: [{
                label: 'Temperature Impact on Fuel Efficiency',
                data: [115, 105, 100, 103, 112],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Relative Fuel Consumption (%)'
                    }
                }
            }
        }
    });

    // Traffic Impact Chart
    const trafficCtx = document.getElementById('trafficChart').getContext('2d');
    new Chart(trafficCtx, {
        type: 'bar',
        data: {
            labels: ['No Traffic', 'Light', 'Moderate', 'Heavy', 'Severe'],
            datasets: [{
                label: 'Traffic Impact on Fuel Consumption',
                data: [100, 110, 125, 150, 180],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(255, 205, 86, 0.5)',
                    'rgba(255, 159, 64, 0.5)',
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(153, 102, 255, 0.5)'
                ]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Relative Fuel Consumption (%)'
                    }
                }
            }
        }
    });

    // Elevation Impact Chart
    const elevationCtx = document.getElementById('elevationChart').getContext('2d');
    new Chart(elevationCtx, {
        type: 'line',
        data: {
            labels: ['-10%', '-5%', '0%', '5%', '10%'],
            datasets: [{
                label: 'Elevation Grade Impact',
                data: [80, 90, 100, 130, 160],
                borderColor: 'rgb(153, 102, 255)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Relative Fuel Consumption (%)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Road Grade'
                    }
                }
            }
        }
    });

    // Combined Factors Chart
    const combinedCtx = document.getElementById('combinedChart').getContext('2d');
    new Chart(combinedCtx, {
        type: 'radar',
        data: {
            labels: ['Temperature', 'Traffic', 'Elevation', 'Weather', 'Road Condition'],
            datasets: [{
                label: 'Best Conditions',
                data: [100, 100, 100, 100, 100],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                pointBackgroundColor: 'rgb(75, 192, 192)'
            }, {
                label: 'Worst Conditions',
                data: [115, 180, 160, 125, 140],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgb(255, 99, 132)',
                pointBackgroundColor: 'rgb(255, 99, 132)'
            }]
        },
        options: {
            responsive: true,
            elements: {
                line: {
                    borderWidth: 3
                }
            }
        }
    });
});