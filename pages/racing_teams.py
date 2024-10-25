import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_timeline import st_timeline
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data, get_constructor_standings_data, get_constructor_drivers_data

# Configuration de la page
st.set_page_config(page_title="Suivi des écuries", layout="wide")

# Titre de la page
st.title("Suivi des écuries")

# Récupérer les DataFrames depuis st.session_state
session_data = get_session_state_data(['constructors', 'constructors_chronology', 'seasons_constructors_standings', 'engine_manufacturers', 'seasons_entrants_driver', 'drivers'])

# Préparation des données
df_constructors = session_data['constructors']
df_chronology = session_data['constructors_chronology']
df_season_standings = session_data['seasons_constructors_standings']
df_engine_manufacturers = session_data['engine_manufacturers']
df_seasons_entrants_driver = session_data['seasons_entrants_driver']
df_drivers = session_data['drivers']
# Ajout d'un filtre pour sélectionner plusieurs constructeurs
constructeurs_selectionnes = st.multiselect(
    "Sélectionnez un ou plusieurs constructeurs",
    options=sorted(df_constructors['fullName'].unique().tolist())
)

if not constructeurs_selectionnes:
    st.warning("🚦 Veuillez sélectionner au moins une écurie.")
else:
    # Initialisation d'un DataFrame vide pour stocker les résultats
    df_all_constructors = pd.DataFrame()
    df_all_constructors_drivers = pd.DataFrame()

    # Appel de la fonction pour chaque constructeur sélectionné
    for constructeur in constructeurs_selectionnes:
        df_constructor_standings = get_constructor_standings_data(constructeur, df_constructors, df_chronology, df_season_standings, df_engine_manufacturers, df_seasons_entrants_driver)
        df_all_constructors = pd.concat([df_all_constructors, df_constructor_standings])
    
    for constructeur in constructeurs_selectionnes:
        df_constructor_drivers = get_constructor_drivers_data(constructeur, df_constructors, df_chronology, df_seasons_entrants_driver, df_drivers)
        df_all_constructors_drivers = pd.concat([df_all_constructors_drivers, df_constructor_drivers])

    # Préparation des données pour le graphique
    df_graph = df_all_constructors.sort_values(['id_constructeur', 'year'])

    # Fusionner df_graph avec df_all_constructors_drivers pour obtenir les informations des pilotes
    df_graph = pd.merge(df_graph, df_all_constructors_drivers[['year', 'id_constructeur', 'driverName']], 
                        on=['year', 'id_constructeur'], how='left')

    # Grouper les pilotes par année et constructeur
    df_graph['drivers'] = df_graph.groupby(['year', 'id_constructeur'])['driverName'].transform(lambda x: ', '.join(x.dropna().unique()))

    # Création du graphique
    fig = px.line(df_graph, x='year', y='positionNumber', color='id_constructeur',
                  title="Évolution des positions des constructeurs au fil des années",
                  labels={'year': 'Année', 'positionNumber': 'Position', 'constructorName': 'Constructeur', 'id_constructeur': 'Ecurie'},
                  markers=True,
                  hover_data=['constructorName', 'engineManufacturerName', 'points', 'drivers'])

    # Inversion de l'axe y pour que la meilleure position (1) soit en haut
    fig.update_yaxes(autorange="reversed")

    # Personnalisation de la toolbox
    fig.update_traces(
        hovertemplate="<b><i>%{customdata[0]}</i></b><br>" +
                      "<b>Année</b>: %{x}<br>" +
                      "<b>Position</b>: %{y}<br>" +
                      "<b>Motoriste</b>: %{customdata[1]}<br>" +
                      "<b>Points</b>: %{customdata[2]}<br>" +
                      "<b>Pilotes</b>: %{customdata[3]}<extra></extra>"
    )

    # Affichage du graphique
    st.plotly_chart(fig)

    # Création d'un tableau des pilotes pour chaque écurie
    st.markdown("### 👨‍🚀 Pilotes par écurie")

    # Créer une liste de paires de constructeurs
    paires_constructeurs = [constructeurs_selectionnes[i:i+2] for i in range(0, len(constructeurs_selectionnes), 2)]
    
    for paire in paires_constructeurs:
        cols = st.columns(2)
        
        for i, constructeur in enumerate(paire):
            with cols[i]:
                st.subheader(f"Pilotes de {constructeur}")
                
                # Filtrer les données pour le constructeur actuel
                df_constructeur = df_all_constructors_drivers[df_all_constructors_drivers['id_constructeur'] == constructeur]
                
                # Afficher le tableau
                st.dataframe(df_constructeur[['year', 'driverName', 'testDriver']].set_index('year'), use_container_width=True)
        
        st.markdown("---")