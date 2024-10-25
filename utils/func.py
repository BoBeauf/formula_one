import streamlit as st
import pandas as pd

# Fonction pour récupérer les données de session_state
# Cette fonction récupère les données stockées dans st.session_state pour les clés spécifiées
# Elle permet d'accéder facilement aux DataFrames stockés globalement dans l'application
# Paramètres:
#   - keys: liste des clés des DataFrames à récupérer
# Retourne:
#   Un dictionnaire contenant les DataFrames demandés, avec les clés comme noms
# @st.cache_data
def get_session_state_data(keys):
    """Récupère les données de st.session_state pour les clés spécifiées et les met en cache."""
    return {key: st.session_state.get(key) for key in keys}

# Fonction pour obtenir les données de classement des constructeurs
# Cette fonction filtre et prépare les données pour un constructeur spécifique
# Elle combine les informations des différentes tables pour créer un DataFrame complet
# Paramètres:
#   - nom_constructeur: le nom complet du constructeur à analyser
#   - df_constructors: DataFrame contenant les informations sur les constructeurs
#   - df_chronology: DataFrame contenant la chronologie des constructeurs
#   - df_season_standings: DataFrame contenant les classements des constructeurs par saison
#   - df_engine_manufacturers: DataFrame contenant les informations sur les motoristes
# Retourne:
#   Un DataFrame filtré et formaté avec les données de classement du constructeur spécifié
def get_constructor_standings_data(nom_constructeur, df_constructors, df_chronology, df_season_standings, df_engine_manufacturers, df_seasons_entrants_driver):
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

    # Ajouter nom_constructeur à l'output
    df_season_standings_filtered['id_constructeur'] = nom_constructeur

    return df_season_standings_filtered

def get_constructor_drivers_data(nom_constructeur, df_constructors, df_chronology, df_seasons_entrants_driver, df_drivers):
    # Application du filtre
    df_constructors_filtered = df_constructors[df_constructors['fullName'] == nom_constructeur]
    parent_constructor_ids = df_constructors_filtered['id'].tolist()

    # Récupération des constructorId correspondants dans la chronologie
    constructor_ids = df_chronology[df_chronology['parentConstructorId'].isin(parent_constructor_ids)]['constructorId'].unique().tolist()

    # Si la liste est vide, utiliser les parent_constructor_ids
    if not constructor_ids:
        constructor_ids = parent_constructor_ids

    df_seasons_entrants_driver_filtered = df_seasons_entrants_driver[df_seasons_entrants_driver['constructorId'].isin(constructor_ids)]
    df_seasons_entrants_driver_filtered = df_seasons_entrants_driver_filtered[['year', 'driverId', 'testDriver']]

    # Fusionner avec df_drivers pour obtenir les vrais noms des pilotes
    df_seasons_entrants_driver_filtered = pd.merge(
        df_seasons_entrants_driver_filtered,
        df_drivers[['id', 'fullName']],
        left_on='driverId',
        right_on='id',
        how='left'
    )

    # Renommer la colonne pour plus de clarté
    df_seasons_entrants_driver_filtered = df_seasons_entrants_driver_filtered.rename(columns={'fullName': 'driverName'})

    # Réorganiser les colonnes
    df_seasons_entrants_driver_filtered = df_seasons_entrants_driver_filtered[['year', 'driverName', 'testDriver']]

    # Ajouter nom_constructeur à l'output
    df_seasons_entrants_driver_filtered['id_constructeur'] = nom_constructeur

    return df_seasons_entrants_driver_filtered