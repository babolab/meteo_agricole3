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
        formatted = {
            'timestamps': [],
            'temperatures': [],
            'precipitation': [],
            'wind_speed': [],
            'humidity': []
        }
        
        if isinstance(raw_data, list):
            for entry in raw_data:
                if isinstance(entry, dict):
                    formatted['timestamps'].append(str(entry.get('datetime', '')))
                    formatted['temperatures'].append(float(entry.get('temperature', 0)))
                    formatted['precipitation'].append(float(entry.get('precipitation', 0)))
                    formatted['wind_speed'].append(float(entry.get('wind_speed', 0)))
                    formatted['humidity'].append(float(entry.get('humidity', 0)))

            if not formatted['timestamps']:
                raise ValueError("Aucune donnée n'a pu être extraite")
                
            return formatted
        else:
            raise ValueError(f"Format de données non supporté: {type(raw_data)}")

    except Exception as e:
        print(f"Erreur lors du formatage: {str(e)}")
        raise

@app.route('/api/weather')
def get_weather():
    try:
        print("\n=== Début de la récupération des données météo ===")
        weather_data = weather_service.get_weather_data()
        if not weather_data:
            raise ValueError("Aucune donnée météo reçue du service")
        print(f"Données brutes reçues: {weather_data}")

        print("\n=== Traitement des données ===")
        processed_data = data_processor.process_data(weather_data)
        if not processed_data:
            raise ValueError("Erreur lors du traitement des données")
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
