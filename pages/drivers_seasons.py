import streamlit as st
import pandas as pd
import altair as alt
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data

# Configuration de la page
st.set_page_config(page_title="Évolution des Pilotes par saison", layout="wide")

# Récupérer les DataFrames depuis st.session_state
session_data = get_session_state_data(['driver_standings', 'seasons_entrants_driver'])

# Ajouter constructorId et rounds à session_data['driver_standings'] en appliquant les règles de sélection
def select_constructor(group):
    # Trier par le nombre de rounds (décroissant) puis par le round le plus bas (croissant)
    group = group.sort_values(by=['rounds', 'roundsText'], ascending=[False, True])
    return group.iloc[0]

# Appliquer la fonction de sélection pour chaque groupe de pilotes par année
selected_entrants = session_data['seasons_entrants_driver'].groupby(['year', 'driverId']).apply(select_constructor).reset_index(drop=True)

# Fusionner les données sélectionnées avec driver_standings
session_data['driver_standings'] = session_data['driver_standings'].merge(
    selected_entrants[['year', 'driverId', 'constructorId', 'rounds']],
    on=['year', 'driverId'],
    how='left'
)

# Titre de la page
st.title("Évolution des Pilotes par saison")

# Permettre à l'utilisateur de sélectionner des pilotes
pilotes_disponibles = session_data['driver_standings']['driverId'].unique()
pilotes_selectionnes = st.multiselect("Sélectionnez les pilotes à afficher", pilotes_disponibles)

# Filtrer les données pour les pilotes sélectionnés
classement_pilotes_selectionnes = session_data['driver_standings'][session_data['driver_standings']['driverId'].isin(pilotes_selectionnes)]

st.markdown("### 🏆 Positions des pilotes au championnat")

if not classement_pilotes_selectionnes.empty:
    # Préparer les données pour Altair
    data_chart = classement_pilotes_selectionnes.pivot(index='year', columns='driverId', values='positionDisplayOrder').reset_index().melt('year', var_name='Pilote', value_name='Position')

    # Ajouter les informations du constructeur
    data_chart = data_chart.merge(
        session_data['driver_standings'][['year', 'driverId', 'constructorId']],
        left_on=['year', 'Pilote'],
        right_on=['year', 'driverId'],
        how='left'
    )

    # Créer le graphique avec Altair
    chart = alt.Chart(data_chart).mark_line(point=True).encode(
        x=alt.X('year:O', title='Année'),
        y=alt.Y('Position:Q', title='Position', scale=alt.Scale(reverse=True)),
        color='Pilote:N',
        tooltip=['year:O', 'Pilote:N', 'Position:Q', 'constructorId:N']
    ).properties(
        width=800,
        height=400
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Veuillez sélectionner au moins un pilote pour afficher le graphique.")

st.markdown("### 🚗 Ecuries des pilotes")

if not classement_pilotes_selectionnes.empty:
    # Préparer les données pour le deuxième graphique
    data_chart_ecuries = classement_pilotes_selectionnes.pivot(index='year', columns='driverId', values='constructorId').reset_index().melt('year', var_name='Pilote', value_name='Écurie')

    # Créer le deuxième graphique avec Altair pour montrer les changements d'écuries
    chart_ecuries = alt.Chart(data_chart_ecuries).mark_line(point=True).encode(
        x=alt.X('year:O', title='Année'),
        y=alt.Y('Écurie:N', title='Écurie'),
        color='Pilote:N',
        tooltip=['year:O', 'Pilote:N', 'Écurie:N']
    ).properties(
        width=800,
        height=400
    ).interactive()

    st.altair_chart(chart_ecuries, use_container_width=True)
else:
    st.info("Veuillez sélectionner au moins un pilote pour afficher le graphique des changements d'écuries.")
