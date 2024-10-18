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

# Trier les résultats par position
resultats_tries = resultats_course.sort_values('positionText')

# Afficher le classement des pilotes
st.subheader(f"Classement des pilotes pour {selected_gp} {annee_selectionnee}")

# Permettre à l'utilisateur de choisir le système de points
systemes_points = [col.split('_', 1)[1] for col in resultats_tries.columns if col.startswith('points_') and not col.startswith('points_cumules_') and not col.endswith('_meilleur_tour')]
points_choisis = st.selectbox("Choisissez le système de points", systemes_points)

# Permettre à l'utilisateur de choisir d'inclure le point bonus
utiliser_bonus = st.checkbox("Inclure le point bonus pour le meilleur tour", value=True)

# Définir les colonnes d'affichage et les noms de colonnes
if utiliser_bonus:
    colonnes_affichage = ['driverId', 'positionText', f'points_{points_choisis}', f'points_cumules_{points_choisis}_meilleur_tour']
    noms_colonnes = {
        'driverId': 'Pilote',
        'positionText': 'Position',
        f'points_{points_choisis}': 'Points',
        f'points_cumules_{points_choisis}_meilleur_tour': 'Points cumulés avec bonus'
    }
else:
    colonnes_affichage = ['driverId', 'positionText', f'points_{points_choisis}', f'points_cumules_{points_choisis}']
    noms_colonnes = {
        'driverId': 'Pilote',
        'positionText': 'Position',
        f'points_{points_choisis}': 'Points',
        f'points_cumules_{points_choisis}': 'Points cumulés'
    }

# Vérifier si le système de points choisi est disponible
if f'points_{points_choisis}' not in resultats_tries.columns or (utiliser_bonus and f'points_cumules_{points_choisis}_meilleur_tour' not in resultats_tries.columns):
    colonnes_affichage = ['driverId', 'positionText']
    noms_colonnes = {
        'driverId': 'Pilote',
        'positionText': 'Position'
    }
    st.warning(f"Les points pour le système {points_choisis} ne sont pas disponibles pour cette course.")

# Créer un DataFrame pour l'affichage
classement_df = resultats_tries[colonnes_affichage].sort_values(by=[col for col in colonnes_affichage if col.startswith('points_cumules_')][0], ascending=False)
classement_df = classement_df.rename(columns=noms_colonnes)

# Afficher le tableau
st.dataframe(classement_df, use_container_width=True)