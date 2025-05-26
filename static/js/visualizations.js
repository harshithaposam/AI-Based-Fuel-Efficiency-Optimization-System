class DataVisualizer {
    constructor() {
        this.charts = {};
    }

    // Route Analysis Chart
    createRouteAnalysisChart(containerId, data) {
        const ctx = document.getElementById(containerId).getContext('2d');
        this.charts.routeAnalysis = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.routes.map(route => route.name),
                datasets: [
                    {
                        label: 'Fuel Consumption (L)',
                        data: data.routes.map(route => route.fuelConsumption),
                        backgroundColor: 'rgba(75, 192, 192, 0.5)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'CO2 Emissions (kg)',
                        data: data.routes.map(route => route.emissions),
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Weather Impact Chart
    createWeatherImpactChart(containerId, data) {
        const ctx = document.getElementById(containerId).getContext('2d');
        this.charts.weatherImpact = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.timestamps,
                datasets: [
                    {
                        label: 'Temperature (°C)',
                        data: data.temperatures,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    },
                    {
                        label: 'Fuel Efficiency Impact (%)',
                        data: data.impacts,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }

    // Traffic Analysis Chart
    createTrafficAnalysisChart(containerId, data) {
        const ctx = document.getElementById(containerId).getContext('2d');
        this.charts.trafficAnalysis = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Morning Rush', 'Midday', 'Evening Rush', 'Night', 'Weekend'],
                datasets: [{
                    label: 'Traffic Impact',
                    data: data.trafficImpact,
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)'
                }]
            },
            options: {
                elements: {
                    line: {
                        borderWidth: 3
                    }
                }
            }
        });
    }

    // Elevation Profile Chart
    createElevationProfileChart(containerId, elevationData) {
        const ctx = document.getElementById(containerId).getContext('2d');
        this.charts.elevationProfile = new Chart(ctx, {
            type: 'line',
            data: {
                labels: elevationData.distances,
                datasets: [{
                    label: 'Elevation (m)',
                    data: elevationData.elevations,
                    fill: true,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Distance (km)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Elevation (m)'
                        }
                    }
                }
            }
        });
    }

    // Fuel Efficiency Trends Chart
    createEfficiencyTrendsChart(containerId, data) {
        const ctx = document.getElementById(containerId).getContext('2d');
        this.charts.efficiencyTrends = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.dates,
                datasets: [{
                    label: 'Average Fuel Efficiency (km/L)',
                    data: data.efficiency,
                    borderColor: 'rgb(153, 102, 255)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    }

    updateChart(chartName, newData) {
        if (this.charts[chartName]) {
            this.charts[chartName].data = newData;
            this.charts[chartName].update();
        }
    }

    destroyChart(chartName) {
        if (this.charts[chartName]) {
            this.charts[chartName].destroy();
            delete this.charts[chartName];
        }
    }
}

// Initialize visualizer
const visualizer = new DataVisualizer();