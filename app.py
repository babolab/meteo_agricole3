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

@app.route('/api/weather')
def get_weather():
    try:
        weather_data = weather_service.get_weather_data()
        print("Données brutes:", weather_data)  # Debug raw data
        
        processed_data = data_processor.process_data(weather_data)
        print("Données traitées:", processed_data)  # Debug processed data
        
        # Vérification de la structure des données
        required_fields = ['timestamps', 'temperatures', 'precipitation', 'wind_speed', 'humidity']
        missing_fields = [field for field in required_fields if field not in processed_data]
        
        if missing_fields:
            raise ValueError(f"Champs manquants dans les données: {missing_fields}")
            
        return jsonify(processed_data)
    except Exception as e:
        import traceback
        print("Erreur détaillée:", traceback.format_exc())  # Debug detailed error
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    next_update = data_processor.get_next_update_time()
    return render_template('index.html',
                         current_time=current_time,
                         next_update=next_update)

if __name__ == '__main__':
    app.run(debug=True)
