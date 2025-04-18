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
        const windTrace1 = {
            x: data.timestamps,
            y: data.arpege.wind_speed,
            type: 'scatter',
            name: 'Arpège',
            line: { color: '#2196F3' }
        };
        
        const windTrace2 = {
            x: data.timestamps,
            y: data.ecmwf.wind_speed,
            type: 'scatter',
            name: 'ECMWF',
            line: { color: '#f44336' }
        };
        
        Plotly.newPlot('windChart', [windTrace1, windTrace2], {
            title: 'Vitesse du vent',
            yaxis: { title: 'km/h' }
        });

        // Humidité
        const humidityTrace1 = {
            x: data.timestamps,
            y: data.arpege.humidity,
            type: 'scatter',
            name: 'Arpège',
            line: { color: '#2196F3' }
        };
        
        const humidityTrace2 = {
            x: data.timestamps,
            y: data.ecmwf.humidity,
            type: 'scatter',
            name: 'ECMWF',
            line: { color: '#f44336' }
        };
        
        Plotly.newPlot('humidityChart', [humidityTrace1, humidityTrace2], {
            title: 'Humidité relative',
            yaxis: { title: '%', range: [0, 100] }
        });

        // Pression atmosphérique
        const pressureTrace1 = {
            x: data.timestamps,
            y: data.arpege.pressure,
            type: 'scatter',
            name: 'Arpège',
            line: { color: '#2196F3' }
        };
        
        const pressureTrace2 = {
            x: data.timestamps,
            y: data.ecmwf.pressure,
            type: 'scatter',
            name: 'ECMWF',
            line: { color: '#f44336' }
        };
        
        Plotly.newPlot('pressureChart', [pressureTrace1, pressureTrace2], {
            title: 'Pression atmosphérique',
            yaxis: { title: 'hPa' }
        });

        // Point de rosée
        const dewpointTrace1 = {
            x: data.timestamps,
            y: data.arpege.dewpoint,
            type: 'scatter',
            name: 'Arpège',
            line: { color: '#2196F3' }
        };
        
        const dewpointTrace2 = {
            x: data.timestamps,
            y: data.ecmwf.dewpoint,
            type: 'scatter',
            name: 'ECMWF',
            line: { color: '#f44336' }
        };
        
        Plotly.newPlot('dewpointChart', [dewpointTrace1, dewpointTrace2], {
            title: 'Point de rosée',
            yaxis: { title: '°C' }
        });

        // Radiation
        const radiationTrace1 = {
            x: data.timestamps,
            y: data.arpege.radiation,
            type: 'scatter',
            name: 'Arpège',
            line: { color: '#2196F3' }
        };
        
        const radiationTrace2 = {
            x: data.timestamps,
            y: data.ecmwf.radiation,
            type: 'scatter',
            name: 'ECMWF',
            line: { color: '#f44336' }
        };
        
        Plotly.newPlot('radiationChart', [radiationTrace1, radiationTrace2], {
            title: 'Radiation solaire directe',
            yaxis: { title: 'W/m²' }
        });

        // ETP
        const etpTrace1 = {
            x: data.timestamps,
            y: data.arpege.etp,
            type: 'scatter',
            name: 'Arpège',
            line: { color: '#2196F3' }
        };
        
        const etpTrace2 = {
            x: data.timestamps,
            y: data.ecmwf.etp,
            type: 'scatter',
            name: 'ECMWF',
            line: { color: '#f44336' }
        };
        
        Plotly.newPlot('etpChart', [etpTrace1, etpTrace2], {
            title: 'Évapotranspiration potentielle',
            yaxis: { title: 'mm' }
        });

        // VPD
        const vpdTrace1 = {
            x: data.timestamps,
            y: data.arpege.vpd,
            type: 'scatter',
            name: 'Arpège',
            line: { color: '#2196F3' }
        };
        
        const vpdTrace2 = {
            x: data.timestamps,
            y: data.ecmwf.vpd,
            type: 'scatter',
            name: 'ECMWF',
            line: { color: '#f44336' }
        };
        
        Plotly.newPlot('vpdChart', [vpdTrace1, vpdTrace2], {
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
                    <th rowspan="2">Date/Heure</th>
                    <th colspan="2">Température</th>
                    <th colspan="2">Précipitations</th>
                    <th colspan="2">Vent</th>
                    <th colspan="2">Direction</th>
                    <th colspan="2">Humidité</th>
                    <th colspan="2">Pression</th>
                    <th colspan="2">Point de rosée</th>
                    <th colspan="2">Radiation</th>
                    <th colspan="2">ETP</th>
                    <th colspan="2">VPD</th>
                    <th rowspan="2">Confiance</th>
                </tr>
                <tr>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                    <th>Arpège</th>
                    <th>ECMWF</th>
                </tr>
            </thead>
            <tbody>
                ${data.timestamps.map((time, i) => `
                    <tr>
                        <td>${new Date(time).toLocaleString('fr-FR')}</td>
                        <td>${data.arpege.temperatures[i]}°C</td>
                        <td>${data.ecmwf.temperatures[i]}°C</td>
                        <td>${data.arpege.precipitation[i]} mm</td>
                        <td>${data.ecmwf.precipitation[i]} mm</td>
                        <td>${data.arpege.wind_speed[i]} km/h</td>
                        <td>${data.ecmwf.wind_speed[i]} km/h</td>
                        <td>${data.arpege.wind_direction[i]}</td>
                        <td>${data.ecmwf.wind_direction[i]}</td>
                        <td>${data.arpege.humidity[i]}%</td>
                        <td>${data.ecmwf.humidity[i]}%</td>
                        <td>${Math.round(data.arpege.pressure[i])} hPa</td>
                        <td>${Math.round(data.ecmwf.pressure[i])} hPa</td>
                        <td>${Math.round(data.arpege.dewpoint[i] * 10) / 10}°C</td>
                        <td>${Math.round(data.ecmwf.dewpoint[i] * 10) / 10}°C</td>
                        <td>${Math.round(data.arpege.radiation[i])} W/m²</td>
                        <td>${Math.round(data.ecmwf.radiation[i])} W/m²</td>
                        <td>${Math.round(data.arpege.etp[i] * 10) / 10} mm</td>
                        <td>${Math.round(data.ecmwf.etp[i] * 10) / 10} mm</td>
                        <td>${Math.round(data.arpege.vpd[i] * 100) / 100} kPa</td>
                        <td>${Math.round(data.ecmwf.vpd[i] * 100) / 100} kPa</td>
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
