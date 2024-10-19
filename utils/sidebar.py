import streamlit as st
from utils.func import get_session_state_data

def sidebar_filters(races, grands_prix, circuits):
    # selected_gp = st.session_state.get('selected_gp')
    # annee_selectionnee = st.session_state.get('annee_selectionnee')
    # gp_races = st.session_state.get('gp_races')
    # gp_details = st.session_state.get('gp_details')
    # circuit_id = st.session_state.get('circuit_id')
    # circuit_details = st.session_state.get('circuit_details')
    # Sélecteur pour choisir une année spécifique
    annees_disponibles = sorted(races['year'].unique(), reverse=True)
    annee_selectionnee = st.sidebar.selectbox("Choisissez une année", annees_disponibles, index=st.session_state.get('annee_selectionnee_index', 0))
    st.session_state['annee_selectionnee_index'] = annees_disponibles.index(annee_selectionnee)

    # Filtrer les courses pour l'année sélectionnée
    courses_annee = races[races['year'] == annee_selectionnee]

    # Mettre à jour le sélecteur de Grand Prix pour n'afficher que ceux de l'année sélectionnée
    grands_prix_annee = courses_annee['grandPrixId'].unique()
    grands_prix_concat = grands_prix[grands_prix['id'].isin(grands_prix_annee)].copy()
    courses_annee = courses_annee.set_index('grandPrixId')
    grands_prix_concat['name_round'] = courses_annee.loc[grands_prix_concat['id'], 'round'].astype(str).values + " - " + grands_prix_concat['name']
    grands_prix_concat['round_number'] = grands_prix_concat['name_round'].apply(lambda x: int(x.split(" - ")[0]))
    grands_prix_concat = grands_prix_concat.sort_values(by='round_number')
    selected_gp_name_round = st.sidebar.selectbox("Choisissez un Grand Prix pour plus de détails", grands_prix_concat['name_round'])
    selected_gp = grands_prix_concat[grands_prix_concat['name_round'] == selected_gp_name_round]['name'].values[0]

    # Afficher les détails du Grand Prix sélectionné
    gp_details = grands_prix[grands_prix['name'] == selected_gp].iloc[0]
    gp_races = races[(races['grandPrixId'] == gp_details['id']) & (races['year'] == annee_selectionnee)]
    # Obtenir les détails du circuit pour le Grand Prix sélectionné
    circuit_id = gp_races.iloc[0]['circuitId']
    circuit_details = circuits[circuits['id'] == circuit_id].iloc[0]

    if st.sidebar.button("Valider la sélection"):
        st.session_state['annee_selectionnee'] = annee_selectionnee
        st.session_state['selected_gp'] = selected_gp
        st.session_state['gp_details'] = gp_details
        st.session_state['gp_races'] = gp_races
        st.session_state['circuit_id'] = circuit_id
        st.session_state['circuit_details'] = circuit_details