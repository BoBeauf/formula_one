import streamlit as st
import pandas as pd
from typing import Tuple
from utils.sidebar import sidebar_filters

# Configuration de la page
st.set_page_config(page_title="Analyse des Grands Prix de F1", layout="wide")

# Récupérer les DataFrames depuis st.session_state
grands_prix = st.session_state.get('grands_prix')
races = st.session_state.get('races')
circuits = st.session_state.get('circuits')
races_results = st.session_state.get('races_results')
points_systems = st.session_state.get('points_systems')


sidebar_filters(races, grands_prix, circuits)
selected_gp = st.session_state.get('selected_gp')
annee_selectionnee = st.session_state.get('annee_selectionnee')
gp_details = st.session_state.get('gp_details')
gp_races = st.session_state.get('gp_races')
circuit_id = st.session_state.get('circuit_id')
circuit_details = st.session_state.get('circuit_details')

# Fonction pour calculer les différents scores
@st.cache_data
def calculer_scores(resultats_course: pd.DataFrame, points_systems: pd.DataFrame) -> pd.DataFrame:
    systemes = points_systems.columns[1:]  # Ignorer la colonne 'position'

    for systeme in systemes:
        resultats_course[f'points_{systeme}'] = resultats_course['positionText'].apply(
            lambda x: points_systems.loc[points_systems['position'] == int(x), systeme].values[0] 
            if x.isdigit() and int(x) <= 20 else 0
        )
        # Ajouter le point pour le meilleur tour
        resultats_course[f'points_{systeme}_meilleur_tour'] = resultats_course[f'points_{systeme}']
        resultats_course.loc[
            (resultats_course['fastestLap'] == True) & (resultats_course['positionText'].apply(lambda x: x.isdigit() and int(x) <= 10)),
            f'points_{systeme}_meilleur_tour'
        ] += 1

    points_cumules = resultats_course.groupby(['year', 'driverId'])

    for systeme in systemes:
        resultats_course[f'points_cumules_{systeme}'] = points_cumules[f'points_{systeme}'].transform('cumsum')
        resultats_course[f'points_cumules_{systeme}_meilleur_tour'] = points_cumules[f'points_{systeme}_meilleur_tour'].transform('cumsum')

    return resultats_course

# Appliquer la fonction aux résultats de course
st.session_state['races_results'] = calculer_scores(races_results, points_systems)

# Obtenir les résultats pour la course sélectionnée
course_selectionnee = gp_races[gp_races['year'] == annee_selectionnee].iloc[0] if gp_races is not None else None
resultats_course = races_results[
    (races_results['raceId'] == course_selectionnee['id']) &
    (races_results['year'] == annee_selectionnee)
]

# Afficher le classement des pilotes
st.subheader(f"Classement des pilotes pour {selected_gp} {annee_selectionnee}")

# Permettre à l'utilisateur de choisir deux systèmes de points pour comparaison
col1, col2 = st.columns(2)
systemes_points = [col.split('_', 1)[1] for col in resultats_course.columns if col.startswith('points_') and not col.startswith('points_cumules_') and not col.endswith('_meilleur_tour')]
with col1:
    points_choisis_1 = st.selectbox("Choisissez le premier système de points", systemes_points, key='points_choisis_1')
with col2:
    points_choisis_2 = st.selectbox("Choisissez le deuxième système de points", systemes_points, key='points_choisis_2')

# Permettre à l'utilisateur de choisir d'inclure le point bonus
with col1:
    utiliser_bonus_1 = st.checkbox("Inclure le point bonus pour le meilleur tour", value=True, key='utiliser_bonus_1')
with col2:
    utiliser_bonus_2 = st.checkbox("Inclure le point bonus pour le meilleur tour", value=True, key='utiliser_bonus_2')


# Définir les colonnes d'affichage et les noms de colonnes pour le premier système
if utiliser_bonus_1:
    colonnes_affichage_1 = ['driverId', 'positionText', f'points_{points_choisis_1}', f'points_cumules_{points_choisis_1}_meilleur_tour', 'position_pilote_1']
    noms_colonnes_1 = {
        'driverId': 'Pilote',
        'positionText': 'Position course',
        f'points_{points_choisis_1}': 'Points course',
        f'points_cumules_{points_choisis_1}_meilleur_tour': 'Points saison',
        'position_pilote_1': 'Position saison'
    }
else:
    colonnes_affichage_1 = ['driverId', 'positionText', f'points_{points_choisis_1}', f'points_cumules_{points_choisis_1}', 'position_pilote_1']
    noms_colonnes_1 = {
        'driverId': 'Pilote',
        'positionText': 'Position course',
        f'points_{points_choisis_1}': 'Points course',
        f'points_cumules_{points_choisis_1}': 'Points saison',
        'position_pilote_1': 'Position saison'
    }

# Définir les colonnes d'affichage et les noms de colonnes pour le deuxième système
if utiliser_bonus_2:
    colonnes_affichage_2 = ['driverId', 'positionText', f'points_{points_choisis_2}', f'points_cumules_{points_choisis_2}_meilleur_tour', 'position_pilote_2']
    noms_colonnes_2 = {
        'driverId': 'Pilote',
        'positionText': 'Position course',
        f'points_{points_choisis_2}': 'Points course',
        f'points_cumules_{points_choisis_2}_meilleur_tour': 'Points saison',
        'position_pilote_2': 'Position saison'
    }
else:
    colonnes_affichage_2 = ['driverId', 'positionText', f'points_{points_choisis_2}', f'points_cumules_{points_choisis_2}', 'position_pilote_2']
    noms_colonnes_2 = {
        'driverId': 'Pilote',
        'positionText': 'Position course',
        f'points_{points_choisis_2}': 'Points course',
        f'points_cumules_{points_choisis_2}': 'Points saison',
        'position_pilote_2': 'Position saison'
    }

# Calculer la position du pilote en utilisant les points cumulés pour le premier système
resultats_course['position_pilote_1'] = resultats_course[f'points_cumules_{points_choisis_1}_meilleur_tour' if utiliser_bonus_1 else f'points_cumules_{points_choisis_1}'].rank(ascending=False, method='min')

# Calculer la position du pilote en utilisant les points cumulés pour le deuxième système
resultats_course['position_pilote_2'] = resultats_course[f'points_cumules_{points_choisis_2}_meilleur_tour' if utiliser_bonus_2 else f'points_cumules_{points_choisis_2}'].rank(ascending=False, method='min')

# Créer les DataFrames pour l'affichage
classement_df_1 = resultats_course[colonnes_affichage_1].sort_values(by=[col for col in colonnes_affichage_1 if col.startswith('points_cumules_')][0], ascending=False)
classement_df_1 = classement_df_1.rename(columns=noms_colonnes_1)

classement_df_2 = resultats_course[colonnes_affichage_2].sort_values(by=[col for col in colonnes_affichage_2 if col.startswith('points_cumules_')][0], ascending=False)
classement_df_2 = classement_df_2.rename(columns=noms_colonnes_2)

# Ajouter un bouton pour choisir l'affichage des positions et des points
display_race_or_year = st.selectbox("Résultats saison ou saison", options=[True, False], format_func=lambda x: "Saison" if x else "Course", index=0)

# Afficher les tableaux côte à côte
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Classement avec {points_choisis_1}")
    if display_race_or_year:
        st.dataframe(classement_df_1[['Pilote', 'Position saison', 'Points saison']], use_container_width=True, hide_index=True)
    else:
        st.dataframe(classement_df_1[['Pilote', 'Position course', 'Points course']].rename(columns=noms_colonnes_1), use_container_width=True, hide_index=True)

with col2:
    st.subheader(f"Classement avec {points_choisis_2}")
    if display_race_or_year:
        st.dataframe(classement_df_2[['Pilote', 'Position saison', 'Points saison']], use_container_width=True, hide_index=True)
    else:
        st.dataframe(classement_df_2[['Pilote', 'Position course', 'Points course']].rename(columns=noms_colonnes_1), use_container_width=True, hide_index=True)
