document.addEventListener('DOMContentLoaded', function() {
    const chartColor = '#2196F3';

    function updateCharts(data) {
        // Température
        const tempTrace = {
            x: data.timestamps,
            y: data.temperatures,
            type: 'scatter',
            name: 'Température',
            line: { color: chartColor }
        };
        
        Plotly.newPlot('tempChart', [tempTrace], {
            title: 'Évolution de la température',
            yaxis: { title: 'Température (°C)' }
        });

        // Précipitations
        const precipTrace = {
            x: data.timestamps,
            y: data.precipitation,
            type: 'bar',
            name: 'Précipitations',
            marker: { color: chartColor }
        };
        
        Plotly.newPlot('precipChart', [precipTrace], {
            title: 'Précipitations',
            yaxis: { title: 'mm', range: [0, 20] }
        });

        // Vent
        const windTrace = {
            x: data.timestamps,
            y: data.wind_speed,
            type: 'scatter',
            name: 'Vitesse du vent',
            line: { color: chartColor }
        };
        
        Plotly.newPlot('windChart', [windTrace], {
            title: 'Vitesse du vent',
            yaxis: { title: 'km/h' }
        });

        // Humidité
        const humidityTrace = {
            x: data.timestamps,
            y: data.humidity,
            type: 'scatter',
            name: 'Humidité',
            line: { color: chartColor }
        };
        
        Plotly.newPlot('humidityChart', [humidityTrace], {
            title: 'Humidité relative',
            yaxis: { title: '%', range: [0, 100] }
        });

        // Mise à jour du tableau détaillé
        updateDetailedTable(data);
    }

    function updateDetailedTable(data) {
        const table = document.getElementById('detailedData');
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Date/Heure</th>
                    <th>Température</th>
                    <th>Précipitations</th>
                    <th>Vent</th>
                    <th>Humidité</th>
                </tr>
            </thead>
            <tbody>
                ${data.timestamps.map((time, i) => `
                    <tr>
                        <td>${time}</td>
                        <td>${data.temperatures[i]}°C</td>
                        <td>${data.precipitation[i]} mm</td>
                        <td>${data.wind_speed[i]} km/h</td>
                        <td>${data.humidity[i]}%</td>
                    </tr>
                `).join('')}
            </tbody>
        `;
    }

    // Fonction de validation des données
    function validateData(data) {
        const requiredFields = ['timestamps', 'temperatures', 'precipitation', 'wind_speed', 'humidity'];
        const missingFields = requiredFields.filter(field => !data[field]);
        
        if (missingFields.length > 0) {
            throw new Error(`Données manquantes: ${missingFields.join(', ')}`);
        }
        
        if (!Array.isArray(data.timestamps) || data.timestamps.length === 0) {
            throw new Error('Aucune donnée temporelle disponible');
        }
    }

    // Chargement initial des données
    fetch('/api/weather')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Données reçues:", data);
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            validateData(data);
            updateCharts(data);
        })
        .catch(error => {
            console.error('Erreur détaillée:', error);
            alert(`Erreur lors du chargement des données: ${error.message}`);
        });

    // Mise à jour automatique toutes les 15 minutes
    setInterval(() => {
        fetch('/api/weather')
            .then(response => response.json())
            .then(data => updateCharts(data))
            .catch(error => console.error('Erreur lors de la mise à jour des données:', error));
    }, 15 * 60 * 1000);
});
