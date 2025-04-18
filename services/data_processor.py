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
            return {
                "error": True,
                "message": weather_data.get("message", "Erreur inconnue")
            }
            
        return {
            "error": False,
            "arpege": self._format_model_data(weather_data["arpege"]),
            "ecmwf": self._format_model_data(weather_data["ecmwf"]),
            "treatment_windows": self._calculate_treatment_windows(weather_data)
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
