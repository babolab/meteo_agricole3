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
    print(f"Contenu des données brutes: {raw_data}")
    
    try:
        # Si les données sont déjà au bon format
        if isinstance(raw_data, dict) and all(key in raw_data for key in ['timestamps', 'temperatures', 'precipitation', 'wind_speed', 'humidity']):
            return raw_data
            
        # Si les données sont une liste de prévisions
        if isinstance(raw_data, list):
            formatted = {
                'timestamps': [],
                'temperatures': [],
                'precipitation': [],
                'wind_speed': [],
                'humidity': []
            }
            
            for entry in raw_data:
                print(f"Traitement de l'entrée: {entry}")
                # Vérification des clés requises
                if not all(key in entry for key in ['datetime', 'temperature', 'precipitation', 'wind_speed', 'humidity']):
                    print(f"Entrée invalide, clés manquantes: {entry}")
                    continue
                    
                formatted['timestamps'].append(entry['datetime'])
                formatted['temperatures'].append(float(entry['temperature']))
                formatted['precipitation'].append(float(entry['precipitation']))
                formatted['wind_speed'].append(float(entry['wind_speed']))
                formatted['humidity'].append(float(entry['humidity']))
            
            if not formatted['timestamps']:
                raise ValueError("Aucune donnée valide n'a pu être extraite")
                
            print(f"Données formatées: {formatted}")
            return formatted
            
        raise ValueError(f"Format de données non supporté: {type(raw_data)}")
        
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
