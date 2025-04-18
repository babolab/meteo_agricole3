document.addEventListener('DOMContentLoaded', function() {
    // Configuration des couleurs pour les modèles
    const colors = {
        arpege: '#2196F3',
        ecmwf: '#f44336'
    };

    // Initialisation des graphiques
    function initCharts() {
        // Température
        const tempTrace = {
            x: [],
            y: [],
            type: 'scatter',
            name: 'Température',
            line: { color: colors.arpege }
        };
        
        Plotly.newPlot('tempChart', [tempTrace], {
            title: 'Évolution de la température',
            yaxis: { title: 'Température (°C)' }
        });

        // Précipitations
        const precipTrace = {
            x: [],
            y: [],
            type: 'bar',
            name: 'Précipitations',
            marker: { color: colors.arpege }
        };
        
        Plotly.newPlot('precipChart', [precipTrace], {
            title: 'Précipitations',
            yaxis: { title: 'mm', range: [0, 20] }
        });

        // Autres graphiques à implémenter...
    }

    // Initialisation
    initCharts();
});
