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

# Function to get constructor standings data
# This function filters and prepares data for a specific constructor
# It combines information from different tables to create a complete DataFrame with performance statistics
# Parameters:
#   - nom_constructeur: full name of the constructor to analyze
#   - df_constructors: DataFrame containing constructor information
#   - df_chronology: DataFrame containing constructor chronology/history
#   - df_season_standings: DataFrame containing constructor championship standings by season
#   - df_engine_manufacturers: DataFrame containing engine manufacturer information
#   - df_seasons_entrants_driver: DataFrame containing driver entries by season
#   - df_races_results: DataFrame containing race results
#   - df_qualifying_results: DataFrame containing qualifying results
# Returns:
#   A filtered and formatted DataFrame with the specified constructor's standings data including:
#   - Championship positions and points
#   - Race statistics (victories, podiums, DNFs, best finish)
#   - Qualifying statistics (pole positions, best qualifying position)
def get_constructor_standings_data(nom_constructeur, df_constructors, df_chronology, df_season_standings, df_engine_manufacturers, df_seasons_entrants_driver, df_races_results, df_qualifying_results):
    # Application du filtre
    df_constructors_filtered = df_constructors[df_constructors['fullName'] == nom_constructeur]
    parent_constructor_ids = df_constructors_filtered['id'].tolist()

    # Récupération des constructorId correspondants dans la chronologie
    constructor_ids = df_chronology[df_chronology['parentConstructorId'].isin(parent_constructor_ids)]['constructorId'].unique().tolist()

    # Si la liste est vide, utiliser les parent_constructor_ids
    if not constructor_ids:
        constructor_ids = parent_constructor_ids

    # Filter race and qualifying results for the selected constructor
    df_races_results_filtered = df_races_results[df_races_results['constructorId'].isin(constructor_ids)]
    df_qualifying_results_filtered = df_qualifying_results[df_qualifying_results['constructorId'].isin(constructor_ids)]

    # Calculate statistics
    # Best result of the year
    best_result = df_races_results_filtered.groupby(['year', 'constructorId'])['positionNumber'].min().reset_index(name='best_position')
    
    # Number of victories
    victories = df_races_results_filtered[df_races_results_filtered['positionNumber'] == 1].groupby(['year', 'constructorId']).size().reset_index(name='victories')
    
    # Number of DNFs
    dnfs = df_races_results_filtered[df_races_results_filtered['positionText'] == 'DNF'].groupby(['year', 'constructorId']).size().reset_index(name='dnfs')
    
    # Number of podiums
    podiums = df_races_results_filtered[df_races_results_filtered['positionNumber'].isin([1,2,3])].groupby(['year', 'constructorId']).size().reset_index(name='podiums')
    
    # Best qualifying position
    best_qualif = df_qualifying_results_filtered.groupby(['year', 'constructorId'])['positionNumber'].min().reset_index(name='best_qualif_position')
    
    # Number of pole positions
    poles = df_qualifying_results_filtered[df_qualifying_results_filtered['positionNumber'] == 1].groupby(['year', 'constructorId']).size().reset_index(name='pole_positions')

    # Get season standings data
    df_season_standings_filtered = df_season_standings[df_season_standings['constructorId'].isin(constructor_ids)]
    df_season_standings_filtered = df_season_standings_filtered[['year', 'constructorId', 'engineManufacturerId', 'positionNumber', 'points']]

    # Merge all statistics
    stats_merged = df_season_standings_filtered.merge(best_result, on=['year', 'constructorId'], how='left')
    stats_merged = stats_merged.merge(victories, on=['year', 'constructorId'], how='left')
    stats_merged = stats_merged.merge(dnfs, on=['year', 'constructorId'], how='left')
    stats_merged = stats_merged.merge(podiums, on=['year', 'constructorId'], how='left')
    stats_merged = stats_merged.merge(best_qualif, on=['year', 'constructorId'], how='left')
    stats_merged = stats_merged.merge(poles, on=['year', 'constructorId'], how='left')

    # Fill NaN values with 0
    stats_merged = stats_merged.fillna(0)

    # Merge with constructor and engine manufacturer information
    stats_merged = pd.merge(
        stats_merged,
        df_constructors[['id', 'fullName']],
        left_on='constructorId',
        right_on='id',
        how='left'
    )

    stats_merged = pd.merge(
        stats_merged,
        df_engine_manufacturers[['id', 'name']],
        left_on='engineManufacturerId',
        right_on='id',
        how='left'
    )

    # Rename columns for clarity
    stats_merged = stats_merged.rename(columns={
        'fullName': 'constructorName',
        'name': 'engineManufacturerName',
        'positionNumber': 'championship_position'
    })

    # Select and reorder columns
    final_columns = [
        'year', 'constructorName', 'engineManufacturerName', 'championship_position',
        'points', 'best_position', 'victories', 'podiums', 'dnfs',
        'best_qualif_position', 'pole_positions'
    ]
    stats_merged = stats_merged[final_columns]

    # Add constructor identifier
    stats_merged['id_constructeur'] = nom_constructeur

    return stats_merged

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