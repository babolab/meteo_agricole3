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
    
    try:
        # Création d'un jeu de données de test si aucune donnée n'est disponible
        if not raw_data:
            print("Aucune donnée reçue, utilisation de données de test")
            from datetime import datetime, timedelta
            base_time = datetime.now()
            test_data = []
            for i in range(24):  # 24 heures de données
                time = base_time + timedelta(hours=i)
                test_data.append({
                    'datetime': time.strftime("%Y-%m-%d %H:%M"),
                    'temperature': 20 + (i % 10),  # 20-30°C
                    'precipitation': i % 5,  # 0-4mm
                    'wind_speed': 10 + (i % 15),  # 10-25km/h
                    'humidity': 60 + (i % 30)  # 60-90%
                })
            raw_data = test_data
            print("Données de test générées:", test_data)

        formatted = {
            'timestamps': [],
            'temperatures': [],
            'precipitation': [],
            'wind_speed': [],
            'humidity': []
        }
        
        if isinstance(raw_data, list):
            for entry in raw_data:
                try:
                    formatted['timestamps'].append(str(entry.get('datetime', '')))
                    formatted['temperatures'].append(float(entry.get('temperature', 0)))
                    formatted['precipitation'].append(float(entry.get('precipitation', 0)))
                    formatted['wind_speed'].append(float(entry.get('wind_speed', 0)))
                    formatted['humidity'].append(float(entry.get('humidity', 0)))
                except (ValueError, TypeError, AttributeError) as e:
                    print(f"Erreur lors du traitement de l'entrée {entry}: {e}")
                    continue
        
        if not formatted['timestamps']:
            print("Aucune donnée n'a pu être formatée correctement")
            raise ValueError("Impossible de formater les données")
            
        print("Données formatées avec succès")
        return formatted
        
    except Exception as e:
        print(f"Erreur lors du formatage: {str(e)}")
        raise ValueError(f"Erreur lors du formatage des données: {str(e)}")

@app.route('/api/weather')
def get_weather():
    try:
        print("\n=== Début de la récupération des données météo ===")
        weather_data = weather_service.get_weather_data()
        
        if not weather_data:
            raise ValueError("Le service météo n'a retourné aucune donnée")
        print(f"Données brutes reçues: Type={type(weather_data)}")
        print(f"Contenu: {weather_data}")

        print("\n=== Traitement des données ===")
        processed_data = data_processor.process_data(weather_data)
        if not processed_data:
            raise ValueError("Le processeur de données n'a retourné aucune donnée")
        print(f"Type des données traitées: {type(processed_data)}")
        print(f"Structure des données traitées: {processed_data}")

        print("\n=== Formatage des données ===")
        formatted_data = format_weather_data(processed_data)
        
        # Validation finale des données
        if not formatted_data or not all(formatted_data.get(key) for key in ['timestamps', 'temperatures', 'precipitation', 'wind_speed', 'humidity']):
            raise ValueError("Les données formatées sont incomplètes")
            
        print("\n=== Envoi des données ===")
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
