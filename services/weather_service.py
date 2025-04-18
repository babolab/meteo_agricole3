import os
import requests
from datetime import datetime, timedelta

class WeatherService:
    def __init__(self):
        self.lat = 48.539116790205455
        self.lon = 1.8692301603242065
        self.base_url = "https://api.open-meteo.com/v1"
        
    def get_weather_data(self):
        """Récupère les données météo des deux modèles (Arpège et ECMWF)"""
        try:
            # Paramètres communs pour les deux modèles
            params = {
                "latitude": self.lat,
                "longitude": self.lon,
                "hourly": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "surface_pressure",
                    "dewpoint_2m",
                    "direct_radiation",
                    "et0_fao_evapotranspiration"
                ],
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "sunrise",
                    "sunset"
                ],
                "timezone": "Europe/Paris"
            }
            
            # Données Arpège (Météo France)
            arpege_params = params.copy()
            arpege_params["model"] = "meteofrance_arpege_europe"
            arpege_response = self._fetch_data(arpege_params)
            
            # Données ECMWF
            ecmwf_params = params.copy()
            ecmwf_params["model"] = "ecmwf_ifs04"
            ecmwf_response = self._fetch_data(ecmwf_params)
            
            # Vérification que les réponses sont différentes
            if arpege_response == ecmwf_response:
                raise Exception("Les données des deux modèles sont identiques, possible erreur API")
            
            return {
                "arpege": arpege_response,
                "ecmwf": ecmwf_response,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _fetch_data(self, params):
        """Effectue la requête à l'API Open-Meteo"""
        response = requests.get(f"{self.base_url}/forecast", params=params)
        if response.status_code != 200:
            raise Exception(f"Erreur API: {response.status_code}")
            
        data = response.json()
        print(f"Données reçues pour le modèle {params['model']}:")
        print(f"Première température: {data.get('hourly', {}).get('temperature_2m', [])[0] if data.get('hourly', {}).get('temperature_2m') else None}")
        return data
