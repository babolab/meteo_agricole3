document.addEventListener('DOMContentLoaded', function() {
    // Theme handling
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = localStorage.getItem('theme');

    // Set dark theme as default
    const defaultTheme = 'dark';
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark') {
            toggleSwitch.checked = true;
        }
    } else {
        document.documentElement.setAttribute('data-theme', defaultTheme);
        localStorage.setItem('theme', defaultTheme);
        toggleSwitch.checked = true;
    }

    function switchTheme(e) {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
        updateChartsTheme();
    }

    toggleSwitch.addEventListener('change', switchTheme, false);

    // Chart colors based on theme
    function getChartColor() {
        return document.documentElement.getAttribute('data-theme') === 'dark' ? '#90caf9' : '#2196F3';
    }
    
    let chartColor = getChartColor();

    function updateChartsTheme() {
        chartColor = getChartColor();
        updateCharts(lastData);
    }

    let lastData = null;
    function updateCharts(data) {
        lastData = data;
        
        // Température
        const tempTrace1 = {
            x: data.timestamps,
            y: data.arpege.temperatures,
            type: 'scatter',
            name: 'Arpège',
            line: { color: '#2196F3' }
        };
        
        const tempTrace2 = {
            x: data.timestamps,
            y: data.ecmwf.temperatures,
            type: 'scatter',
            name: 'ECMWF',
            line: { color: '#f44336' }
        };
        
        Plotly.newPlot('tempChart', [tempTrace1, tempTrace2], {
            title: 'Évolution de la température',
            yaxis: { title: 'Température (°C)' }
        });

        // Précipitations
        const precipTrace1 = {
            x: data.timestamps,
            y: data.arpege.precipitation,
            type: 'bar',
            name: 'Arpège',
            marker: { color: '#2196F3' }
        };
        
        const precipTrace2 = {
            x: data.timestamps,
            y: data.ecmwf.precipitation,
            type: 'bar',
            name: 'ECMWF',
            marker: { color: '#f44336' }
        };
        
        Plotly.newPlot('precipChart', [precipTrace1, precipTrace2], {
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

        // Pression atmosphérique
        const pressureTrace = {
            x: data.timestamps,
            y: data.pressure,
            type: 'scatter',
            name: 'Pression',
            line: { color: chartColor }
        };
        
        Plotly.newPlot('pressureChart', [pressureTrace], {
            title: 'Pression atmosphérique',
            yaxis: { title: 'hPa' }
        });

        // Point de rosée
        const dewpointTrace = {
            x: data.timestamps,
            y: data.dewpoint,
            type: 'scatter',
            name: 'Point de rosée',
            line: { color: chartColor }
        };
        
        Plotly.newPlot('dewpointChart', [dewpointTrace], {
            title: 'Point de rosée',
            yaxis: { title: '°C' }
        });

        // Radiation
        const radiationTrace = {
            x: data.timestamps,
            y: data.radiation,
            type: 'scatter',
            name: 'Radiation',
            line: { color: chartColor }
        };
        
        Plotly.newPlot('radiationChart', [radiationTrace], {
            title: 'Radiation solaire directe',
            yaxis: { title: 'W/m²' }
        });

        // ETP
        const etpTrace = {
            x: data.timestamps,
            y: data.etp,
            type: 'scatter',
            name: 'ETP',
            line: { color: chartColor }
        };
        
        Plotly.newPlot('etpChart', [etpTrace], {
            title: 'Évapotranspiration potentielle',
            yaxis: { title: 'mm' }
        });

        // VPD
        const vpdTrace = {
            x: data.timestamps,
            y: data.vpd,
            type: 'scatter',
            name: 'VPD',
            line: { color: chartColor }
        };
        
        Plotly.newPlot('vpdChart', [vpdTrace], {
            title: 'Déficit de pression de vapeur',
            yaxis: { title: 'kPa' }
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
                    <th>Direction</th>
                    <th>Humidité</th>
                    <th>Pression</th>
                    <th>Point de rosée</th>
                    <th>Radiation</th>
                    <th>ETP</th>
                    <th>VPD</th>
                    <th>Indice de confiance</th>
                </tr>
            </thead>
            <tbody>
                ${data.timestamps.map((time, i) => `
                    <tr>
                        <td>${new Date(time).toLocaleString('fr-FR')}</td>
                        <td>${data.temperatures[i]}°C</td>
                        <td>${data.precipitation[i]} mm</td>
                        <td>${data.wind_speed[i]} km/h</td>
                        <td>${data.wind_direction[i]}</td>
                        <td>${data.humidity[i]}%</td>
                        <td>${Math.round(data.pressure[i])} hPa</td>
                        <td>${Math.round(data.dewpoint[i] * 10) / 10}°C</td>
                        <td>${Math.round(data.radiation[i])} W/m²</td>
                        <td>${Math.round(data.etp[i] * 10) / 10} mm</td>
                        <td>${Math.round(data.vpd[i] * 100) / 100} kPa</td>
                        <td>${data.confidence_index[i]}%</td>
                    </tr>
                `).join('')}
            </tbody>
        `;

        // Mise à jour du calendrier des traitements
        const calendar = document.getElementById('treatmentCalendar');
        if (data.treatment_windows && data.treatment_windows.length > 0) {
            calendar.innerHTML = `
                <div class="alert alert-info">
                    <h4>Fenêtres de traitement recommandées :</h4>
                    <ul>
                        ${data.treatment_windows.map(window => `
                            <li>
                                Le ${new Date(window.start).toLocaleString('fr-FR', { timeZone: 'Europe/Paris' })}
                                (Humidité: ${window.humidity}%, 
                                Coucher du soleil: ${new Date(window.sunset).toLocaleString('fr-FR', { timeZone: 'Europe/Paris' })})
                            </li>
                        `).join('')}
                    </ul>
                </div>
            `;
        } else {
            calendar.innerHTML = `
                <div class="alert alert-warning">
                    Aucune fenêtre de traitement favorable dans les prochaines 24 heures.
                </div>
            `;
        }
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
