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

sidebar_filters(races, grands_prix, circuits, driver_standings)
selected_gp = st.session_state.get('selected_gp')
annee_selectionnee = st.session_state.get('annee_selectionnee')
gp_races = st.session_state.get('gp_races')
gp_details = st.session_state.get('gp_details')
circuit_id = st.session_state.get('circuit_id')
circuit_details = st.session_state.get('circuit_details')
pilotes_annee = st.session_state.get('pilotes_annee')

st.markdown("---")
st.markdown("### 🏁 Détails du Grand Prix")

if not selected_gp or not annee_selectionnee:
    st.info("🚦 Veuillez sélectionner un Grand Prix pour afficher les détails !")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**🏆 Date:** {gp_races.iloc[0]['date']}")
        st.markdown(f"**🏆 Nom GP:** {gp_details['fullName']}")
        st.markdown(f"**🏆 Nom Race:** {gp_races.iloc[0]['officialName']}")
        st.markdown(f"**🏟️ Nom du Circuit:** {circuit_details['fullName']}")
        st.markdown(f"**📍 Lieu:** {circuit_details['placeName']}")

    with col2:
        st.markdown(f"**🔤 Abréviation:** {gp_details['abbreviation']}")
        st.markdown(f"**🛣️ Type de Circuit:** {circuit_details['type']}")
        st.markdown(f"**🌍 Pays:** {gp_details['countryId']}")
        st.markdown(f"**🏎️ Nombre total de courses:** {circuit_details['totalRacesHeld']}")
        st.markdown(f"**📏 Longueur du circuit:** {gp_races.iloc[0]['courseLength']} km")

    st.markdown("---")