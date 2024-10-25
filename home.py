import streamlit as st
import pandas as pd
from typing import Tuple
from utils.sidebar import sidebar_filters

st.title("Formula 1 Analyzer 🏎️💨")

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
    constructors = pd.read_csv('f1db-csv/f1db-constructors.csv')
    constructors_chronology = pd.read_csv('f1db-csv/f1db-constructors-chronology.csv')
    seasons_constructors_standings = pd.read_csv('f1db-csv/f1db-seasons-constructor-standings.csv')
    engine_manufacturers = pd.read_csv('f1db-csv/f1db-engine-manufacturers.csv')
    seasons_entrants_driver = pd.read_csv('f1db-csv/f1db-seasons-entrants-drivers.csv')
    drivers = pd.read_csv('f1db-csv/f1db-drivers.csv')
    return grands_prix, races, races_results, points_systems, circuits, driver_standings, seasons_entrants_driver, constructors, constructors_chronology, seasons_constructors_standings, engine_manufacturers, seasons_entrants_driver, drivers

grands_prix, races, races_results, points_systems, circuits, driver_standings, seasons_entrants_driver, constructors, constructors_chronology, seasons_constructors_standings, engine_manufacturers, seasons_entrants_driver, drivers = load_data()

# Stocker les DataFrames dans st.session_state
st.session_state['grands_prix'] = grands_prix
st.session_state['races'] = races
st.session_state['races_results'] = races_results
st.session_state['points_systems'] = points_systems
st.session_state['circuits'] = circuits
st.session_state['driver_standings'] = driver_standings
st.session_state['seasons_entrants_driver'] = seasons_entrants_driver
st.session_state['constructors'] = constructors
st.session_state['constructors_chronology'] = constructors_chronology
st.session_state['seasons_constructors_standings'] = seasons_constructors_standings
st.session_state['engine_manufacturers'] = engine_manufacturers
st.session_state['seasons_entrants_driver'] = seasons_entrants_driver
st.session_state['drivers'] = drivers

st.markdown("""
## Bienvenue ! 👋

Je suis votre guide ultime pour plonger dans l'univers fascinant des Grands Prix de Formule 1 !

### 🚀 Fonctionnalités

- **Driver Seasons**:
  - 📈 *Suivez l'évolution du classement au championnat pour les pilotes sélectionnés*
  - 🔄 *Suivez leurs changements d'écuries, saison par saison*
  - 📊 *Comparez les résultats au fil des saisons*

- **Map Seasons**: 
  - 🗺️ *Carte interactive des Grands Prix de l'année sélectionnée*
  - 🌍 *Comparez les déplacements, le nombre de GP depuis l'existence de la F1*

- **Points Systems**: 
  - ⚖️ *Comparez les barèmes de points pour la saison et/ou une course sélectionnée*
  - 📜 *Barèmes de points dispos: anciens F1, motoGP, indycar*
  - 🏁 *Ajoutez ou non le point du fastest lap dans le calcul des classements*
  - ⚠️ *Les courses sprints ne sont pas comptabilisées*
            
- **Racing Teams**:
  - 📈 *Suivez l'évolution des positions des écuries au championnat*
  - 🔄 *Suivez leurs changements de noms, saison par saison*
  - 📊 *Suivez leurs changements de motoristes, saison par saison*
  - 🏎️ *Suivez leurs pilotes, saison par saison*

### 🌐 Source des Données
            
Les données proviennent du **repo F1DB**. Vous pouvez y accéder ici : [F1DB GitHub](https://github.com/f1db/f1db). Elles sont mises à jour **chaque lundi à midi** 🕛 pour vous garantir les informations les plus récentes et précises.

### 🔍 Explorez le Code Source
            
Plongez dans le code source complet de ce projet sur GitHub : [formula_one GitHub](https://github.com/BoBeauf/formula_one). Découvrez comment tout fonctionne sous le capot ! 🚗💨 N'hésitez pas à proposer des améliorations ou des suggestions directement sur GitHub pour contribuer à l'évolution du projet !

### 👨‍💻 Créateur
            
Retrouvez-moi sur [GitHub](https://github.com/BoBeauf) et [LinkedIn](https://www.linkedin.com/in/louis-ledoux-data-analyst/) !

""")
