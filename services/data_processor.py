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
            
        # Récupération des données des deux modèles
        arpege_data = weather_data.get("arpege", {}).get("hourly", {})
        ecmwf_data = weather_data.get("ecmwf", {}).get("hourly", {})
        
        if not arpege_data or not ecmwf_data:
            raise ValueError("Données manquantes pour au moins un modèle")
        
        # Extraction des données horaires pour les deux modèles
        timestamps = arpege_data.get("time", [])
        
        # Modèle Arpège
        arpege_temps = arpege_data.get("temperature_2m", [])
        arpege_precip = arpege_data.get("precipitation", [])
        arpege_wind = arpege_data.get("wind_speed_10m", [])
        arpege_wind_dir = arpege_data.get("wind_direction_10m", [])
        arpege_humidity = arpege_data.get("relative_humidity_2m", [])
        arpege_pressure = arpege_data.get("surface_pressure", [])
        arpege_dewpoint = arpege_data.get("dewpoint_2m", [])
        arpege_radiation = arpege_data.get("direct_radiation", [])
        arpege_etp = arpege_data.get("et0_fao_evapotranspiration", [])
        
        # Modèle ECMWF
        ecmwf_temps = ecmwf_data.get("temperature_2m", [])
        ecmwf_precip = ecmwf_data.get("precipitation", [])
        ecmwf_wind = ecmwf_data.get("wind_speed_10m", [])
        ecmwf_wind_dir = ecmwf_data.get("wind_direction_10m", [])
        ecmwf_humidity = ecmwf_data.get("relative_humidity_2m", [])
        ecmwf_pressure = ecmwf_data.get("surface_pressure", [])
        ecmwf_dewpoint = ecmwf_data.get("dewpoint_2m", [])
        ecmwf_radiation = ecmwf_data.get("direct_radiation", [])
        ecmwf_etp = ecmwf_data.get("et0_fao_evapotranspiration", [])

        # Calcul du VPD pour les deux modèles
        arpege_vpd = self._calculate_vpd(arpege_temps, arpege_humidity)
        ecmwf_vpd = self._calculate_vpd(ecmwf_temps, ecmwf_humidity)
        
        # Vérification des données
        if not timestamps or not arpege_temps or not ecmwf_temps:
            raise ValueError("Données horaires manquantes")
            
        # Calcul des fenêtres de traitement (basé sur Arpège)
        treatment_windows = self._calculate_treatment_windows(weather_data)
            
        # Conversion des directions du vent en notation cardinale
        arpege_wind_dir_cardinal = [self._degrees_to_cardinal(d) if d is not None else 'N/A' for d in arpege_wind_dir]
        ecmwf_wind_dir_cardinal = [self._degrees_to_cardinal(d) if d is not None else 'N/A' for d in ecmwf_wind_dir]

        # Calcul de l'indice de confiance
        confidence_index = self._calculate_confidence_index(weather_data)

        return {
            'timestamps': timestamps,
            'arpege': {
                'temperatures': arpege_temps,
                'precipitation': arpege_precip,
                'wind_speed': arpege_wind,
                'wind_direction': arpege_wind_dir_cardinal,
                'humidity': arpege_humidity,
                'pressure': arpege_pressure,
                'dewpoint': arpege_dewpoint,
                'radiation': arpege_radiation,
                'etp': arpege_etp,
                'vpd': arpege_vpd
            },
            'ecmwf': {
                'temperatures': ecmwf_temps,
                'precipitation': ecmwf_precip,
                'wind_speed': ecmwf_wind,
                'wind_direction': ecmwf_wind_dir_cardinal,
                'humidity': ecmwf_humidity,
                'pressure': ecmwf_pressure,
                'dewpoint': ecmwf_dewpoint,
                'radiation': ecmwf_radiation,
                'etp': ecmwf_etp,
                'vpd': ecmwf_vpd
            },
            'treatment_windows': treatment_windows,
            'confidence_index': confidence_index
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
        wind_speed = hourly.get("wind_speed_10m", [])
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
                
            # Vérifie si l'heure est proche du coucher du soleil
            time_diff = (time_dt - sunset).total_seconds() / 3600
            
            # Conditions générales favorables
            is_favorable = humidity[i] >= 70 and wind_speed[i] < 20
            
            # Conditions spécifiques pour le colza
            is_colza_favorable = (
                is_favorable and 
                -2 <= time_diff <= 3  # 2h avant à 3h après le coucher du soleil
            )
            
            if is_favorable:
                window_type = "colza" if is_colza_favorable else "general"
                windows.append({
                    'start': time,
                    'humidity': humidity[i],
                    'wind_speed': wind_speed[i],
                    'sunset': sunset.strftime("%Y-%m-%d %H:%M"),
                    'type': window_type
                })
        
        return windows

    def _degrees_to_cardinal(self, degrees):
        """Convertit les degrés en direction cardinale"""
        if degrees is None:
            return 'N/A'
        
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSO', 'SO', 'OSO', 'O', 'ONO', 'NO', 'NNO']
        index = round(degrees / (360 / len(directions))) % len(directions)
        return directions[index]

    def _calculate_vpd(self, temperatures, humidity):
        """Calcule le déficit de pression de vapeur (VPD)"""
        vpd = []
        for t, h in zip(temperatures, humidity):
            if t is None or h is None:
                vpd.append(None)
                continue
            
            # Pression de vapeur saturante (kPa)
            es = 0.6108 * pow(2.7183, (17.27 * t) / (t + 237.3))
            # Pression de vapeur réelle (kPa)
            ea = es * (h / 100)
            # VPD (kPa)
            vpd.append(round(es - ea, 3))
        
        return vpd

    def _calculate_confidence_index(self, weather_data):
        """Calcule l'indice de confiance basé sur la concordance des modèles"""
        arpege = weather_data.get("arpege", {}).get("hourly", {})
        ecmwf = weather_data.get("ecmwf", {}).get("hourly", {})
        
        if not arpege or not ecmwf:
            return []
            
        confidence = []
        params = [
            ('temperature_2m', 2),  # différence acceptable de 2°C
            ('precipitation', 5),   # différence acceptable de 5mm
            ('wind_speed_10m', 10)  # différence acceptable de 10km/h
        ]
        
        for i in range(len(arpege.get('time', []))):
            score = 0
            total = 0
            
            for param, threshold in params:
                a_val = arpege.get(param, [])[i] if i < len(arpege.get(param, [])) else None
                e_val = ecmwf.get(param, [])[i] if i < len(ecmwf.get(param, [])) else None
                
                if a_val is not None and e_val is not None:
                    diff = abs(a_val - e_val)
                    score += 1 if diff <= threshold else 0
                    total += 1
            
            confidence.append(round(score / total * 100) if total > 0 else 0)
        
        return confidence
