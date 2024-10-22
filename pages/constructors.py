import streamlit as st
import pandas as pd
import plotly.express as px
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data

# Configuration de la page
st.set_page_config(page_title="Constructeurs", layout="wide")

# Titre de la page
st.title("Constructeurs")

# Récupérer les DataFrames depuis st.session_state
session_data = get_session_state_data(['constructors', 'constructors_chronology', 'seasons_constructors_standings', 'engine_manufacturers'])

# Préparation des données
df_constructors = session_data['constructors']
df_chronology = session_data['constructors_chronology']
df_season_standings = session_data['seasons_constructors_standings']
df_engine_manufacturers = session_data['engine_manufacturers']

# Ajout d'un filtre pour le nom complet du constructeur
nom_constructeur = st.selectbox(
    "Sélectionnez un constructeur",
    options=sorted(df_constructors['fullName'].unique().tolist())
)

# Application du filtre
df_constructors_filtered = df_constructors[df_constructors['fullName'] == nom_constructeur]
parent_constructor_ids = df_constructors_filtered['id'].tolist()

# Récupération des constructorId correspondants dans la chronologie
constructor_ids = df_chronology[df_chronology['parentConstructorId'].isin(parent_constructor_ids)]['constructorId'].unique().tolist()

# Si la liste est vide, utiliser les parent_constructor_ids
if not constructor_ids:
    constructor_ids = parent_constructor_ids

df_season_standings_filtered = df_season_standings[df_season_standings['constructorId'].isin(constructor_ids)]
df_season_standings_filtered = df_season_standings_filtered[['year', 'constructorId', 'engineManufacturerId', 'positionNumber', 'points']]

# Effectuer un left join entre df_season_standings_filtered et df_constructors
df_season_standings_filtered = pd.merge(
    df_season_standings_filtered,
    df_constructors[['id', 'fullName']],
    left_on='constructorId',
    right_on='id',
    how='left'
)

df_season_standings_filtered = pd.merge(
    df_season_standings_filtered,
    df_engine_manufacturers[['id', 'name']],
    left_on='engineManufacturerId',
    right_on='id',
    how='left'
)

# Renommer les colonnes pour plus de clarté
df_season_standings_filtered = df_season_standings_filtered.rename(columns={'fullName': 'constructorName', 'name': 'engineManufacturerName'})

# Réorganiser les colonnes pour une meilleure lisibilité
df_season_standings_filtered = df_season_standings_filtered[['year', 'constructorName', 'engineManufacturerName', 'positionNumber', 'points']]

# Préparation des données pour le graphique
df_graph = df_season_standings_filtered.sort_values('year')

# Création du graphique
fig = px.line(df_graph, x='year', y='positionNumber', 
              title=f"Évolution des positions de {nom_constructeur} au fil des années",
              labels={'year': 'Année', 'positionNumber': 'Position'},
              markers=True)

# Inversion de l'axe y pour que la meilleure position (1) soit en haut
fig.update_yaxes(autorange="reversed")

# Affichage du graphique
st.plotly_chart(fig)

st.dataframe(df_season_standings_filtered)