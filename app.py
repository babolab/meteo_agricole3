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
        processed_data = data_processor.process_data(weather_data)
        print("Données météo récupérées:", processed_data)  # Debug log
        return jsonify(processed_data)
    except Exception as e:
        print("Erreur lors de la récupération des données:", str(e))  # Debug log
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
