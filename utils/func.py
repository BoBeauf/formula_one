import streamlit as st

# @st.cache_data
def get_session_state_data(keys):
    """Récupère les données de st.session_state pour les clés spécifiées et les met en cache."""
    return {key: st.session_state.get(key) for key in keys}