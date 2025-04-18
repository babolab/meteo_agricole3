from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self):
        self.update_interval = timedelta(hours=1)
    
    def get_next_update_time(self):
        """Calcule l'heure de la prochaine mise à jour"""
        now = datetime.now()
        next_hour = (now + self.update_interval).replace(minute=0, second=0, microsecond=0)
        return next_hour.strftime("%d/%m/%Y %H:%M")
    
    def process_data(self, weather_data):
        """Traite les données météo pour l'affichage"""
        if weather_data.get("status") == "error":
            raise ValueError(weather_data.get("message", "Erreur inconnue"))
            
        # On utilise les données Arpège par défaut
        arpege_data = weather_data.get("arpege", {})
        hourly_data = arpege_data.get("hourly", {})
        
        # Extraction des données horaires
        timestamps = hourly_data.get("time", [])
        temperatures = hourly_data.get("temperature_2m", [])
        precipitation = hourly_data.get("precipitation", [])
        wind_speed = hourly_data.get("wind_speed_10m", [])
        humidity = hourly_data.get("relative_humidity_2m", [])
        
        # Vérification des données
        if not timestamps or not temperatures:
            raise ValueError("Données horaires manquantes")
            
        return {
            'timestamps': timestamps,
            'temperatures': temperatures,
            'precipitation': precipitation,
            'wind_speed': wind_speed,
            'humidity': humidity
        }
    
    def _format_model_data(self, model_data):
        """Formate les données d'un modèle pour l'affichage"""
        return {
            "hourly": model_data["hourly"],
            "daily": model_data["daily"]
        }
    
    def _calculate_treatment_windows(self, weather_data):
        """Calcule les fenêtres favorables aux traitements"""
        windows = []
        
        # Logique à implémenter pour identifier les périodes propices
        # basée sur l'hygrométrie ≥ 70% et les heures de coucher du soleil
        
        return windows
