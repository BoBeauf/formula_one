import streamlit as st
import pandas as pd
from typing import Tuple
from utils.sidebar import sidebar_filters

st.title("Analyse des Grands Prix de Formule 1")

# Charger les données
@st.cache_data
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    grands_prix = pd.read_csv('f1db-csv/f1db-grands-prix.csv')
    races_results = pd.read_csv('f1db-csv/f1db-races-race-results.csv')
    races = pd.read_csv('f1db-csv/f1db-races.csv')
    points_systems = pd.read_csv('f1db-csv/points_systems.csv')
    circuits = pd.read_csv('f1db-csv/f1db-circuits.csv')
    driver_standings = pd.read_csv('f1db-csv/f1db-seasons-driver-standings.csv')
    seasons_entrants_driver = pd.read_csv('f1db-csv/f1db-seasons-entrants-drivers.csv')
    return grands_prix, races, races_results, points_systems, circuits, driver_standings, seasons_entrants_driver

grands_prix, races, races_results, points_systems, circuits, driver_standings, seasons_entrants_driver = load_data()

# Stocker les DataFrames dans st.session_state
st.session_state['grands_prix'] = grands_prix
st.session_state['races'] = races
st.session_state['races_results'] = races_results
st.session_state['points_systems'] = points_systems
st.session_state['circuits'] = circuits
st.session_state['driver_standings'] = driver_standings
st.session_state['seasons_entrants_driver'] = seasons_entrants_driver

st.markdown("""
## Présentation de l'application

Bienvenue dans notre application d'analyse des Grands Prix de Formule 1 ! Cette application est conçue pour vous fournir une vue d'ensemble complète des courses de Formule 1, en vous permettant d'explorer les résultats des courses, les systèmes de points, et bien plus encore.

### Fonctionnalités principales

- **Analyse des Courses**: Visualisez les résultats des courses passées et comparez les performances des pilotes.
- **Systèmes de Points**: Comparez différents systèmes de points pour voir comment ils affectent le classement des pilotes.
- **Détails des Circuits**: Obtenez des informations détaillées sur chaque circuit, y compris le lieu, le type de circuit, et la longueur.
- **Classement des Pilotes**: Affichez le classement des pilotes pour une saison ou une course spécifique, avec la possibilité d'inclure des points bonus pour le meilleur tour.

### Comment utiliser l'application

1. **Sélectionnez un Grand Prix**: Utilisez la barre latérale pour choisir un Grand Prix et une année.
2. **Explorez les Détails**: Consultez les détails du Grand Prix sélectionné, y compris le nom, la date, et le circuit.
3. **Comparez les Systèmes de Points**: Choisissez deux systèmes de points pour voir comment ils influencent le classement des pilotes.
4. **Visualisez les Classements**: Affichez les classements des pilotes en fonction des systèmes de points sélectionnés.

Nous espérons que vous trouverez cette application utile pour approfondir votre compréhension des Grands Prix de Formule 1. Profitez de l'exploration des données et des analyses !

""")
