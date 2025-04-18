
# Cahier des Charges Détaillé - Version amendée

## Présentation du Projet

Le projet consiste à développer une page web dédiée aux agriculteurs fournissant des données météorologiques précises pour la position géographique 48.539116790205455, 1.8692301603242065 (située près d'Ablis, Île-de-France). Cette solution vise à faciliter la prise de décision agricole en offrant des prévisions météorologiques issues des modèles Arpège (7 jours) et ECMWF (10 jours).

## Objectifs Principaux

- Fournir aux agriculteurs un accès simple et rapide aux données météorologiques pertinentes
- Présenter les prévisions des modèles Arpège (7 jours) et ECMWF (10 jours)
- Permettre la comparaison visuelle entre les deux modèles
- Identifier les périodes propices aux traitements agricoles selon des critères spécifiques
- Héberger la page web sur GitHub Pages avec mise à jour automatique toutes les heures
- Assurer la compatibilité avec tous les appareils (responsive design)
- Afficher l'heure de génération et du prochain calcul en haut de la page
- Fournir une URL fixe et pérenne


## Spécifications Techniques

### Architecture et Hébergement

- **Plateforme d'hébergement**: GitHub Pages
- **Automatisation**: GitHub Actions pour la génération et le déploiement automatique
- **Fréquence de mise à jour**: Toutes les heures
- **Format responsive**: Compatible avec ordinateurs, tablettes et smartphones
- **Persistance des préférences**: LocalStorage pour le thème utilisateur
- **Réalité des données**: Utilisation exclusive de données réelles avec indication claire en cas d'indisponibilité


### Acquisition des Données

- **Sources de données**:
  - API Météo France pour le modèle Arpège
  - API ECMWF pour le modèle européen
  - Alternative: API openmeteo pour récupérer les données de ces modèles
- **Paramètres à récupérer**:
  - Température (°C) avec min/max journalière
  - Précipitations (mm)
  - Vent (force en km/h et direction en degrés)
  - Hygrométrie (%)
  - Point de rosée
  - Pression atmosphérique
  - Évapotranspiration potentielle (ETP)
  - Heures de lever et coucher du soleil
  - Rayonnement global à la surface
  - Déficit de pression de vapeur (VPD) - paramètre important pour l'agriculture


### Interface Utilisateur

#### En-tête

- **Informations principales**:
  - Titre du service: "Météo Agricole - Ablis"
  - Coordonnées géographiques précises avec nom de la localité
  - Date et heure de dernière mise à jour (format français)
  - Heure prévue du prochain calcul (format français)
  - Sélecteur de thème clair/sombre


#### Section Graphiques

- **Système d'onglets** permettant de basculer entre:
  - Vue comparative (les deux modèles superposés)
  - Vue Arpège uniquement
  - Vue ECMWF uniquement
- **Graphiques interactifs**:
  - **Température**: Courbe d'évolution avec échelle en °C, affichage des min/max
  - **Précipitations**: Histogramme avec échelle en mm (0-20mm)
  - **Vent**: Courbe de vitesse en km/h avec flèches directionnelles
  - **Hygrométrie**: Courbe d'évolution (0-100%)
  - **Radar de pluie**: Visualisation des précipitations en temps réel (si disponible via API)
- **Code couleur**:
  - Modèle Arpège: Bleu (\#2196F3)
  - Modèle ECMWF: Rouge (\#f44336)


#### Section Tableaux de Données

- **Tableau horizontal** présentant les données par tranche horaire:
  - Organisation par jour et par tranche horaire (1h)
  - Colonnes pour chaque paramètre (température, précipitations, vent, hygrométrie)
  - Coloration des cellules selon les valeurs (ex: température, force du vent)
  - Affichage de la direction du vent en notation cardinale (N, NE, E, SE, etc.)
  - Format similaire à celui utilisé sur Météociel pour une prise en main rapide


#### Section Périodes Propices aux Traitements

- **Calendrier visuel** sur 10 jours indiquant:
  - Périodes favorables aux traitements généraux (hygrométrie ≥ 70%)
  - Périodes spécifiques pour le traitement du colza (2h avant à 3h après le coucher du soleil avec hygrométrie ≥ 70%)
  - Code couleur intuitif (vert: optimal, orange: partiellement favorable, rouge: défavorable)
- **Tableau récapitulatif** des créneaux optimaux:
  - Date et heures précises
  - Durée estimée de la fenêtre d'intervention
  - Paramètres météo prévus pendant cette période
  - Indice de confiance basé sur la concordance des deux modèles




### Développement Technique

- **Frontend**:
  - HTML5, CSS3 (avec framework responsive comme Bootstrap)
  - JavaScript pour l'interactivité et les graphiques (Chart.js ou D3.js)
  - Système de thème clair/sombre avec détection automatique des préférences système
- **Backend/Automatisation**:
  - Script Python pour la récupération des données et génération de la page statique
  - GitHub Actions pour l'exécution horaire du script
  - Stockage temporaire des données pour afficher l'historique récent même en cas de panne API
- **Performance**:
  - Optimisation des images et ressources
  - Mise en cache appropriée
  - Chargement progressif des éléments (lazy loading)


## Contraintes Techniques

- **Performance**: Temps de chargement inférieur à 3 secondes
- **Accessibilité**: Interface intuitive ne nécessitant aucune compétence technique
- **Compatibilité navigateurs**: Chrome, Firefox, Safari, Edge (versions récentes)
- **Sécurité**: Aucune donnée utilisateur collectée ou stockée
- **Disponibilité**: Gestion des cas de défaillance des API avec affichage de messages appropriés


## Livrables Attendus

1. **Code source** complet sur dépôt GitHub
   - Structure du projet claire et documentée
   - Commentaires explicatifs dans le code
   - Tests automatisés pour vérifier la récupération et l'affichage des données
2. **Documentation technique** détaillant:
   - L'architecture du système
   - Les sources de données et méthodes d'acquisition
   - Les procédures de déploiement et de mise à jour
   - Guide de dépannage en cas de problème
3. **URL de la page web** fonctionnelle et accessible publiquement
4. **Guide utilisateur** expliquant:
   - L'interprétation des données et graphiques
   - La signification des codes couleur et indicateurs
   - Comment utiliser efficacement les informations pour planifier les interventions agricoles

