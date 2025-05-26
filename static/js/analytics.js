class AnalyticsDashboard {
    constructor() {
        this.period = 'week';
        this.charts = {};
        this.websocket = null;
        this.initializeWebSocket();
        this.initializeCharts();
        this.setupEventListeners();
        this.loadData();
    }

    initializeWebSocket() {
        this.websocket = new WebSocket(
            `ws://${window.location.host}/ws/analytics/`
        );

        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };
    }

    initializeCharts() {
        // Efficiency Trends Chart
        this.charts.efficiencyTrends = new Chart(
            document.getElementById('efficiencyTrendsChart').getContext('2d'),
            {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Efficiency Score',
                        data: [],
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            }
        );

        // Environmental Impact Chart
        this.charts.environmentalImpact = new Chart(
            document.getElementById('environmentalImpactChart').getContext('2d'),
            {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'CO2 Emissions Saved (kg)',
                        data: [],
                        backgroundColor: 'rgba(75, 192, 192, 0.5)'
                    }]
                },
                options: {
                    responsive: true
                }
            }
        );

        // Initialize other charts similarly
    }

    setupEventListeners() {
        document.querySelectorAll('[data-period]').forEach(button => {
            button.addEventListener('click', () => {
                this.period = button.dataset.period;
                this.loadData();
            });
        });
    }

    async loadData() {
        try {
            const response = await fetch(`/api/analytics/?period=${this.period}`);
            const data = await response.json();
            this.updateDashboard(data);
        } catch (error) {
            console.error('Error loading analytics data:', error);
        }
    }

    updateDashboard(data) {
        this.updateMetrics(data.metrics);
        this.updateCharts(data.charts);
        this.updateRecentRoutes(data.recent_routes);
    }

    updateMetrics(metrics) {
        document.getElementById('totalRoutes').textContent = metrics.total_routes;
        document.getElementById('fuelSaved').textContent = `${metrics.fuel_saved}L`;
        document.getElementById('co2Reduced').textContent = `${metrics.co2_reduced}kg`;
        document.getElementById('efficiencyScore').textContent = metrics.efficiency_score;

        // Update change percentages
        this.updateChangeMetric('routesChange', metrics.routes_change);
        this.updateChangeMetric('fuelChange', metrics.fuel_change);
        this.updateChangeMetric('co2Change', metrics.co2_change);
        this.updateChangeMetric('efficiencyChange', metrics.efficiency_change);
    }

    updateChangeMetric(elementId, change) {
        const element = document.getElementById(elementId);
        const value = change >= 0 ? `+${change}%` : `${change}%`;
        element.textContent = value;
        element.className = `metric-change ${change >= 0 ? 'positive' : 'negative'}`;
    }

    updateCharts(chartData) {
        // Update Efficiency Trends
        this.charts.efficiencyTrends.data.labels = chartData.efficiency.labels;
        this.charts.efficiencyTrends.data.datasets[0].data = chartData.efficiency.data;
        this.charts.efficiencyTrends.update();

        // Update Environmental Impact
        this.charts.environmentalImpact.data.labels = chartData.environmental.labels;
        this.charts.environmentalImpact.data.datasets[0].data = chartData.environmental.data;
        this.charts.environmentalImpact.update();

        // Update other charts similarly
    }

    updateRecentRoutes(routes) {
        const tbody = document.querySelector('#recentRoutesTable tbody');
        tbody.innerHTML = routes.map(route => `
            <tr>
                <td>${new Date(route.created_at).toLocaleDateString()}</td>
                <td>${route.source} to ${route.destination}</td>
                <td>${route.distance} km</td>
                <td>${route.fuel_consumption} L</td>
                <td>${route.carbon_emissions} kg</td>
                <td>${route.efficiency_score}</td>
            </tr>
        `).join('');
    }

    handleWebSocketMessage(data) {
        if (data.type === 'route_update') {
            this.loadData();  // Reload all data when a new route is added
        }
    }
}

// Initialize dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new AnalyticsDashboard();
});