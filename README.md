# Météo Agricole - Ablis

Application web fournissant des prévisions météorologiques détaillées pour les agriculteurs d'Ablis et ses environs. Le service combine les données des modèles Arpège (Météo France) et ECMWF pour offrir des prévisions précises et identifier les périodes propices aux traitements agricoles.

## Fonctionnalités

- 🌡️ Prévisions détaillées sur 7-10 jours (température, précipitations, vent, hygrométrie...)
- 📊 Visualisation comparative des modèles Arpège et ECMWF
- 🎯 Identification automatique des périodes favorables aux traitements
- 📱 Interface responsive (ordinateur, tablette, smartphone)
- 🔄 Mise à jour automatique toutes les heures

## Installation

### Prérequis

- Python 3.12+
- Git

### Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/meteo-agricole.git
cd meteo-agricole

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur Linux/Mac :
# source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration

1. Créer un fichier `.env` à la racine du projet :
```env
FLASK_ENV=development
```

### Lancement

```bash
python app.py
```

L'application sera accessible à l'adresse : http://localhost:5000

## Déploiement

Le site est automatiquement déployé sur GitHub Pages via GitHub Actions à chaque push sur la branche main.

URL de production : https://votre-username.github.io/meteo-agricole/

## Structure du Projet


```
meteo-agricole/
├── .github/
│   └── workflows/        # Configuration GitHub Actions
├── services/
│   ├── weather_service.py    # Service de récupération des données météo
│   └── data_processor.py     # Traitement des données
├── static/
│   ├── css/             # Styles CSS
│   └── js/              # Scripts JavaScript
├── templates/           # Templates HTML
├── .env                 # Configuration locale
├── .gitignore
├── app.py              # Application Flask
├── requirements.txt    # Dépendances Python
└── README.md
```

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -am 'Ajout de fonctionnalité'`)
4. Push la branche (`git push origin feature/amelioration`)
5. Créer une Pull Request

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.
