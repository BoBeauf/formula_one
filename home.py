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
    qualifying_results = pd.read_csv('f1db-csv/f1db-races-qualifying-results.csv')
    return grands_prix, races, races_results, points_systems, circuits, driver_standings, seasons_entrants_driver, constructors, constructors_chronology, seasons_constructors_standings, engine_manufacturers, seasons_entrants_driver, drivers, qualifying_results, season_driver_standings

grands_prix, races, races_results, points_systems, circuits, driver_standings, seasons_entrants_driver, constructors, constructors_chronology, seasons_constructors_standings, engine_manufacturers, seasons_entrants_driver, drivers, qualifying_results, season_driver_standings = load_data()

# Stocker les DataFrames dans st.session_state
st.session_state['grands_prix'] = grands_prix
st.session_state['races'] = races
st.session_state['races_results'] = races_results
st.session_state['points_systems'] = points_systems
st.session_state['circuits'] = circuits
st.session_state['driver_standings'] = driver_standings
st.session_state['season_driver_standings'] = season_driver_standings
st.session_state['seasons_entrants_driver'] = seasons_entrants_driver
st.session_state['constructors'] = constructors
st.session_state['constructors_chronology'] = constructors_chronology
st.session_state['seasons_constructors_standings'] = seasons_constructors_standings
st.session_state['engine_manufacturers'] = engine_manufacturers
st.session_state['seasons_entrants_driver'] = seasons_entrants_driver
st.session_state['drivers'] = drivers
st.session_state['qualifying_results'] = qualifying_results

st.markdown("""
## Welcome! 👋

I am your ultimate guide to dive into the fascinating world of Formula 1 Grand Prix!

            
### 🚀 Features

- **Driver Seasons**:
  - 📈 *Track championship standings evolution for selected drivers*
  - 🔄 *Follow their team changes, season by season*
  - 📊 *Compare results over the seasons*

            
- **Map Seasons**: 
  - 🗺️ *Interactive map of Grand Prix for the selected year*
  - 🌍 *Compare travels, number of GPs since F1's existence*

            
- **Points Systems**: 
  - ⚖️ *Compare points systems for the season and/or selected race*
  - 📜 *Available points systems: old F1, MotoGP, IndyCar*
  - 🏁 *Add or remove fastest lap point in standings calculations*
  - ⚠️ *Sprint races are not counted*

              
- **Racing Teams**:
  - 📈 *Track teams' championship positions evolution*
  - 🔄 *Follow their name changes, season by season*
  - 📊 *Follow their engine manufacturer changes, season by season*
  - 🏎️ *Follow their drivers, season by season*

### 🌐 Data Source
            
Data comes from the **F1DB repo**. You can access it here: [F1DB GitHub](https://github.com/f1db/f1db). It is updated **every Monday at noon** 🕛 to ensure you get the most recent and accurate information.

### 🔍 Explore the Source Code
            
Dive into the complete source code of this project on GitHub: [formula_one GitHub](https://github.com/BoBeauf/formula_one). Discover how everything works under the hood! 🚗💨 Don't hesitate to suggest improvements or suggestions directly on GitHub to contribute to the project's evolution!

### 👨‍💻 Creator
            
Find me on [GitHub](https://github.com/BoBeauf) and [LinkedIn](https://www.linkedin.com/in/louis-ledoux-data-analyst/)!

""")
