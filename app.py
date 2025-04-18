from flask import Flask, render_template, url_for
from datetime import datetime
import os
from dotenv import load_dotenv
from services.weather_service import WeatherService
from services.data_processor import DataProcessor

load_dotenv()

app = Flask(__name__)
weather_service = WeatherService()
data_processor = DataProcessor()

from flask import jsonify

def format_weather_data(raw_data):
    """Structure les données météo dans le format attendu par le frontend"""
    print("\n=== Formatage des données brutes ===")
    print(f"Type des données brutes: {type(raw_data)}")
    print(f"Contenu brut: {raw_data}")
    
    try:
        # Si les données sont déjà au bon format
        if isinstance(raw_data, dict) and all(key in raw_data for key in ['timestamps', 'temperatures', 'precipitation', 'wind_speed', 'humidity']):
            return raw_data

        # Données de test par défaut
        if not raw_data:
            print("Génération de données de test")
            from datetime import datetime, timedelta
            base_time = datetime.now()
            formatted = {
                'timestamps': [],
                'temperatures': [],
                'precipitation': [],
                'wind_speed': [],
                'humidity': []
            }
            
            for i in range(24):
                time = base_time + timedelta(hours=i)
                formatted['timestamps'].append(time.strftime("%Y-%m-%d %H:%M"))
                formatted['temperatures'].append(20 + (i % 10))
                formatted['precipitation'].append(i % 5)
                formatted['wind_speed'].append(10 + (i % 15))
                formatted['humidity'].append(60 + (i % 30))
            
            return formatted

        # Si les données sont une liste d'objets météo
        if isinstance(raw_data, list):
            formatted = {
                'timestamps': [],
                'temperatures': [],
                'precipitation': [],
                'wind_speed': [],
                'humidity': []
            }
            
            for entry in raw_data:
                if isinstance(entry, dict):
                    formatted['timestamps'].append(str(entry.get('datetime', '')))
                    formatted['temperatures'].append(float(entry.get('temperature', 20)))
                    formatted['precipitation'].append(float(entry.get('precipitation', 0)))
                    formatted['wind_speed'].append(float(entry.get('wind_speed', 10)))
                    formatted['humidity'].append(float(entry.get('humidity', 60)))

            if formatted['timestamps']:
                return formatted

        # Si on arrive ici, on utilise des données de test
        print("Format non reconnu, utilisation de données de test")
        return format_weather_data(None)

    except Exception as e:
        print(f"Erreur lors du formatage: {str(e)}")
        print("Utilisation de données de test suite à l'erreur")
        return format_weather_data(None)

@app.route('/api/weather')
def get_weather():
    try:
        print("\n=== Début de la récupération des données météo ===")
        weather_data = weather_service.get_weather_data()
        print(f"Données brutes reçues: {weather_data}")

        print("\n=== Traitement des données ===")
        processed_data = data_processor.process_data(weather_data) if weather_data else None
        print(f"Données traitées: {processed_data}")

        print("\n=== Formatage des données ===")
        formatted_data = format_weather_data(processed_data)
        print(f"Données formatées: {formatted_data}")
        
        return jsonify(formatted_data)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("\n=== ERREUR ===")
        print(f"Type d'erreur: {type(e).__name__}")
        print(f"Message d'erreur: {str(e)}")
        print("Traceback complet:")
        print(error_details)
        return jsonify({
            "error": f"{type(e).__name__}: {str(e)}",
            "details": error_details
        }), 500

@app.route('/')
def index():
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    next_update = data_processor.get_next_update_time()
    return render_template('index.html',
                         current_time=current_time,
                         next_update=next_update)

if __name__ == '__main__':
    app.run(debug=True)
