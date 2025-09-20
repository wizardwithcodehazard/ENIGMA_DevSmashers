// Get score from HTML data attribute
const container = document.getElementById('stabilityChartContainer');
const score = container ? parseInt(container.dataset.score) : 0;

// Render Stability Score chart
const ctx = document.getElementById('stabilityChart');
if (ctx) {
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Stability', 'Remaining'],
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: ['#4CAF50', '#ddd'],
            }]
        },
        options: {
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}
