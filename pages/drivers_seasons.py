import streamlit as st
import pandas as pd
import altair as alt
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data

# Configuration de la page
st.set_page_config(page_title="Évolution du Classement de chaque Pilote", layout="wide")

# Récupérer les DataFrames depuis st.session_state
session_data = get_session_state_data(['driver_standings'])

# Titre de la page
st.title("Évolution du Classement de chaque Pilote")

# Permettre à l'utilisateur de sélectionner des pilotes
pilotes_disponibles = session_data['driver_standings']['driverId'].unique()
pilotes_selectionnes = st.multiselect("Sélectionnez les pilotes à afficher", pilotes_disponibles)

# Filtrer les données pour les pilotes sélectionnés
classement_pilotes_selectionnes = session_data['driver_standings'][session_data['driver_standings']['driverId'].isin(pilotes_selectionnes)]

# Créer un graphique amélioré de l'évolution du classement des pilotes sélectionnés

if not classement_pilotes_selectionnes.empty:
    # Préparer les données pour Altair
    data_chart = classement_pilotes_selectionnes.pivot(index='year', columns='driverId', values='positionDisplayOrder').reset_index().melt('year', var_name='Pilote', value_name='Position')

    # Créer le graphique avec Altair
    chart = alt.Chart(data_chart).mark_line(point=True).encode(
        x=alt.X('year:O', title='Année'),
        y=alt.Y('Position:Q', title='Position', scale=alt.Scale(reverse=True)),
        color='Pilote:N',
        tooltip=['year:O', 'Pilote:N', 'Position:Q']
    ).properties(
        width=800,
        height=400
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Veuillez sélectionner au moins un pilote pour afficher le graphique.")
