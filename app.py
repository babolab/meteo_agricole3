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
    try:
        return {
            'timestamps': [entry['datetime'] for entry in raw_data],
            'temperatures': [entry['temperature'] for entry in raw_data],
            'precipitation': [entry['precipitation'] for entry in raw_data],
            'wind_speed': [entry['wind_speed'] for entry in raw_data],
            'humidity': [entry['humidity'] for entry in raw_data]
        }
    except KeyError as e:
        raise ValueError(f"Champ manquant dans les données brutes: {str(e)}")

@app.route('/api/weather')
def get_weather():
    try:
        print("Récupération des données météo...")
        weather_data = weather_service.get_weather_data()
        print("Données brutes reçues:", weather_data)

        if not weather_data:
            raise ValueError("Aucune donnée météo reçue")

        print("Traitement des données...")
        processed_data = data_processor.process_data(weather_data)
        print("Données traitées:", processed_data)

        print("Formatage des données...")
        formatted_data = format_weather_data(processed_data)
        print("Données formatées:", formatted_data)

        return jsonify(formatted_data)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("Erreur détaillée:", error_details)
        return jsonify({
            "error": str(e),
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
