from flask import Flask, render_template
from datetime import datetime
import os
from dotenv import load_dotenv
from services.weather_service import WeatherService
from services.data_processor import DataProcessor

load_dotenv()

app = Flask(__name__)
weather_service = WeatherService()
data_processor = DataProcessor()

@app.route('/')
def index():
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    next_update = data_processor.get_next_update_time()
    
    weather_data = weather_service.get_weather_data()
    processed_data = data_processor.process_data(weather_data)
    
    return render_template('index.html',
                         current_time=current_time,
                         next_update=next_update,
                         weather_data=processed_data)

if __name__ == '__main__':
    app.run(debug=True)
