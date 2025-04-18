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
            
        # Calcul des fenêtres de traitement
        treatment_windows = self._calculate_treatment_windows(weather_data)
            
        return {
            'timestamps': timestamps,
            'temperatures': temperatures,
            'precipitation': precipitation,
            'wind_speed': wind_speed,
            'humidity': humidity,
            'treatment_windows': treatment_windows
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
        
        arpege_data = weather_data.get("arpege", {})
        hourly = arpege_data.get("hourly", {})
        daily = arpege_data.get("daily", {})
        
        if not hourly or not daily:
            return windows
            
        times = hourly.get("time", [])
        humidity = hourly.get("relative_humidity_2m", [])
        sunsets = daily.get("sunset", [])
        
        # Pour chaque heure
        for i, time in enumerate(times):
            time_dt = datetime.fromisoformat(time)
            
            # Trouve le coucher de soleil correspondant
            sunset = None
            for sunset_time in sunsets:
                sunset_dt = datetime.fromisoformat(sunset_time)
                if sunset_dt.date() == time_dt.date():
                    sunset = sunset_dt
                    break
            
            if not sunset:
                continue
                
            # Vérifie si l'heure est proche du coucher du soleil (±2h)
            time_diff = abs((time_dt - sunset).total_seconds() / 3600)
            
            # Conditions favorables :
            # - Hygrométrie ≥ 70%
            # - Dans les 2 heures avant ou après le coucher du soleil
            if humidity[i] >= 70 and time_diff <= 2:
                windows.append({
                    'start': time,
                    'humidity': humidity[i],
                    'sunset': sunset.strftime("%Y-%m-%d %H:%M")
                })
        
        return windows
