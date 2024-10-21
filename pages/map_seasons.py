import streamlit as st
import pandas as pd
import pydeck as pdk
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data

# Configuration de la page
st.set_page_config(page_title="Carte des Courses par Saison", layout="wide")

# Titre de la page
st.title("Carte des Courses par Saison")

# Récupérer les DataFrames depuis st.session_state
session_data = get_session_state_data(['races', 'circuits', 'grands_prix'])

# Sélecteur pour choisir une année spécifique
annees_disponibles = sorted(session_data['races']['year'].unique(), reverse=True)
annee_selectionnee = st.sidebar.selectbox("Choisissez une année", annees_disponibles, index=0)
st.session_state['annee_selectionnee_index'] = annees_disponibles.index(annee_selectionnee)

# Filtrer les courses pour l'année sélectionnée
courses_annee = session_data['races'][session_data['races']['year'] == annee_selectionnee]

# Obtenir les détails des circuits pour les courses de l'année sélectionnée
circuits_annee = session_data['circuits'][session_data['circuits']['id'].isin(courses_annee['circuitId'].unique())]


# Définir les couleurs pour les épingles avec un gradient de jaune à rouge
def definir_couleur(index, total):
    ratio = index / (total - 1)
    rouge = int(255 * ratio)
    jaune = int(255 * (1 - ratio))
    return [rouge, jaune, 0, 160]

# Trier les courses par date
courses_annee_sorted = courses_annee.sort_values(by='date')
circuits_annee['color'] = [definir_couleur(i, len(circuits_annee)) for i in range(len(circuits_annee))]
line_data = pd.merge(courses_annee_sorted, circuits_annee, left_on='circuitId', right_on='id')

# Créer une carte avec pydeck
scatterplot_layer = pdk.Layer(
    'ScatterplotLayer',
    data=line_data,  # Utiliser line_data pour inclure les informations de course
    get_position='[longitude, latitude]',
    get_radius=150000,  # Augmenter la taille des épingles
    get_color='color',  # Utiliser la couleur définie
    pickable=True
)

# Créer des lignes entre les circuits en utilisant les positions des courses successives
line_data['source_longitude'] = line_data['longitude'].shift()
line_data['source_latitude'] = line_data['latitude'].shift()
line_data = line_data.dropna(subset=['source_longitude', 'source_latitude'])

line_layer = pdk.Layer(
    'LineLayer',
    data=line_data,
    get_source_position='[source_longitude, source_latitude]',
    get_target_position='[longitude, latitude]',
    get_color='[128, 128, 128, 160]',  # Couleur grise pour les lignes
    get_width=1
)

view_state = pdk.ViewState(
    latitude=circuits_annee['latitude'].mean(),
    longitude=circuits_annee['longitude'].mean(),
    zoom=2,
    pitch=0
)

r = pdk.Deck(
    layers=[scatterplot_layer, line_layer],
    initial_view_state=view_state,
    tooltip={"text": "Course {round}: {name}"},  # Afficher le numéro de la course
    map_style='light'  # Carte noire
)

st.pydeck_chart(r)
