import streamlit as st
import pandas as pd
from typing import Tuple
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data

# Configuration de la page
st.set_page_config(page_title="Analyse des Grands Prix de F1", layout="wide")

@st.cache_data
def calculer_scores(resultats_course: pd.DataFrame, points_systems: pd.DataFrame, drivers: pd.DataFrame) -> pd.DataFrame:
    """Calcule les scores des pilotes selon différents systèmes de points."""
    systemes = points_systems.columns[1:]  # Ignorer la colonne 'position'

    for systeme in systemes:
        resultats_course[f'points_{systeme}'] = resultats_course['positionText'].apply(
            lambda x: points_systems.loc[points_systems['position'] == int(x), systeme].values[0] 
            if x.isdigit() and int(x) <= 20 else 0
        )
        # Ajouter le point pour le meilleur tour
        resultats_course[f'points_{systeme}_meilleur_tour'] = resultats_course[f'points_{systeme}']
        resultats_course.loc[
            (resultats_course['fastestLap']) & (resultats_course['positionText'].apply(lambda x: x.isdigit() and int(x) <= 10)),
            f'points_{systeme}_meilleur_tour'
        ] += 1

    points_cumules = resultats_course.groupby(['year', 'driverId'])

    for systeme in systemes:
        resultats_course[f'points_cumules_{systeme}'] = points_cumules[f'points_{systeme}'].transform('cumsum')
        resultats_course[f'points_cumules_{systeme}_meilleur_tour'] = points_cumules[f'points_{systeme}_meilleur_tour'].transform('cumsum')

    return resultats_course

def afficher_classement(resultats_course, points_choisis, utiliser_bonus, col):
    """Affiche le classement des pilotes pour un système de points donné."""
    if utiliser_bonus:
        colonnes_affichage = ['driverId', 'positionText', f'points_{points_choisis}', f'points_cumules_{points_choisis}_meilleur_tour', 'position_pilote']
        noms_colonnes = {
            'driverId': 'Pilote',
            'positionText': 'Position course',
            f'points_{points_choisis}': 'Points course',
            f'points_cumules_{points_choisis}_meilleur_tour': 'Points saison',
            'position_pilote': 'Position saison'
        }
    else:
        colonnes_affichage = ['driverId', 'positionText', f'points_{points_choisis}', f'points_cumules_{points_choisis}', 'position_pilote']
        noms_colonnes = {
            'driverId': 'Pilote',
            'positionText': 'Position course',
            f'points_{points_choisis}': 'Points course',
            f'points_cumules_{points_choisis}': 'Points saison',
            'position_pilote': 'Position saison'
        }

    resultats_course['position_pilote'] = resultats_course[f'points_cumules_{points_choisis}_meilleur_tour' if utiliser_bonus else f'points_cumules_{points_choisis}'].rank(ascending=False, method='min')
    classement_df = resultats_course[colonnes_affichage].rename(columns=noms_colonnes)

    col.subheader(f"Classement avec {points_choisis}")
    if display_race_or_year:
        classement_df_sorted = classement_df[['Pilote', 'Position saison', 'Points saison']].sort_values(by='Points saison', ascending=False)
    else:
        classement_df_sorted = classement_df[['Pilote', 'Position course', 'Points course']].sort_values(by='Points course', ascending=False)
    col.dataframe(classement_df_sorted, use_container_width=True, hide_index=True)


# Récupérer les DataFrames depuis st.session_state
session_data = get_session_state_data(['grands_prix', 'races', 'circuits', 'races_results', 'points_systems', 'selected_gp', 'annee_selectionnee', 'gp_details', 'gp_races', 'circuit_id', 'circuit_details', 'driver_standings', 'pilotes_annee'])

sidebar_filters(session_data['races'], session_data['grands_prix'], session_data['circuits'], session_data['driver_standings'])

session_data = get_session_state_data(['grands_prix', 'races', 'circuits', 'races_results', 'points_systems', 'selected_gp', 'annee_selectionnee', 'gp_details', 'gp_races', 'circuit_id', 'circuit_details', 'driver_standings', 'pilotes_annee'])

if not session_data['selected_gp'] or not session_data['annee_selectionnee']:
    st.info("🚦 Veuillez sélectionner un Grand Prix pour afficher les détails !")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**🏆 Date:** {session_data['gp_races'].iloc[0]['date']}")
        st.markdown(f"**🏆 Nom GP:** {session_data['gp_details']['fullName']}")
        st.markdown(f"**🏆 Nom Race:** {session_data['gp_races'].iloc[0]['officialName']}")
        st.markdown(f"**🏟️ Nom du Circuit:** {session_data['circuit_details']['fullName']}")
        st.markdown(f"**📍 Lieu:** {session_data['circuit_details']['placeName']}")

    with col2:
        st.markdown(f"**🔤 Abréviation:** {session_data['gp_details']['abbreviation']}")
        st.markdown(f"**🛣️ Type de Circuit:** {session_data['circuit_details']['type']}")
        st.markdown(f"**🌍 Pays:** {session_data['gp_details']['countryId']}")
        st.markdown(f"**🏎️ Nombre total de courses:** {session_data['circuit_details']['totalRacesHeld']}")
        st.markdown(f"**📏 Longueur du circuit:** {session_data['gp_races'].iloc[0]['courseLength']} km")

    st.markdown("---")

# Appliquer la fonction aux résultats de course
st.session_state['races_results'] = calculer_scores(session_data['races_results'], session_data['points_systems'], session_data['pilotes_annee'])

# Obtenir les résultats pour la course sélectionnée
course_selectionnee = session_data['gp_races'][session_data['gp_races']['year'] == session_data['annee_selectionnee']].iloc[0] if session_data['gp_races'] is not None else None
resultats_course = session_data['races_results'][
    (session_data['races_results']['raceId'] == course_selectionnee['id']) &
    (session_data['races_results']['year'] == session_data['annee_selectionnee'])
]

# Afficher le classement des pilotes
st.subheader(f"Classement des pilotes pour {session_data['selected_gp']} {session_data['annee_selectionnee']}")

# Ajouter un bouton pour choisir l'affichage des positions et des points
display_race_or_year = st.selectbox("Résultats saison ou course", options=[True, False], format_func=lambda x: "Saison" if x else "Course", index=0)

# Permettre à l'utilisateur de choisir deux systèmes de points pour comparaison
col1, col2 = st.columns(2)
systemes_points = [col.split('_', 1)[1] for col in resultats_course.columns if col.startswith('points_') and not col.startswith('points_cumules_') and not col.endswith('_meilleur_tour')]

with col1:
    points_choisis_1 = st.selectbox("Choisissez le premier système de points", systemes_points, key='points_choisis_1', index=0)
    utiliser_bonus_1 = st.checkbox("Inclure le point bonus pour le meilleur tour", value=True, key='utiliser_bonus_1')
with col2:
    points_choisis_2 = st.selectbox("Choisissez le deuxième système de points", systemes_points, key='points_choisis_2', index=1)
    utiliser_bonus_2 = st.checkbox("Inclure le point bonus pour le meilleur tour", value=True, key='utiliser_bonus_2')

# Afficher les tableaux côte à côte
afficher_classement(resultats_course, points_choisis_1, utiliser_bonus_1, col1)
afficher_classement(resultats_course, points_choisis_2, utiliser_bonus_2, col2)
