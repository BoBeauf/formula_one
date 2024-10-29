import streamlit as st
import pandas as pd
from typing import Tuple
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data

# Page configuration
st.set_page_config(page_title="F1 Grand Prix Analysis", layout="wide")

@st.cache_data
def calculate_scores(race_results: pd.DataFrame, points_systems: pd.DataFrame, drivers: pd.DataFrame) -> pd.DataFrame:
    """Calculate driver scores according to different points systems."""
    systems = points_systems.columns[1:]  # Ignore 'position' column

    for system in systems:
        race_results[f'points_{system}'] = race_results['positionText'].apply(
            lambda x: points_systems.loc[points_systems['position'] == int(x), system].values[0] 
            if x.isdigit() and int(x) <= 20 else 0
        )
        # Add point for fastest lap
        race_results[f'points_{system}_fastest_lap'] = race_results[f'points_{system}']
        race_results.loc[
            (race_results['fastestLap']) & (race_results['positionText'].apply(lambda x: x.isdigit() and int(x) <= 10)),
            f'points_{system}_fastest_lap'
        ] += 1

    cumulative_points = race_results.groupby(['year', 'driverId'])

    for system in systems:
        race_results[f'cumulative_points_{system}'] = cumulative_points[f'points_{system}'].transform('cumsum')
        race_results[f'cumulative_points_{system}_fastest_lap'] = cumulative_points[f'points_{system}_fastest_lap'].transform('cumsum')

    return race_results

def display_standings(race_results, points_chosen, use_bonus, col):
    """Display driver standings for a given points system."""
    if use_bonus:
        display_columns = ['driverId', 'positionText', f'points_{points_chosen}', f'cumulative_points_{points_chosen}_fastest_lap', 'driver_position']
        column_names = {
            'driverId': 'Driver',
            'positionText': 'Race Position',
            f'points_{points_chosen}': 'Race Points',
            f'cumulative_points_{points_chosen}_fastest_lap': 'Season Points',
            'driver_position': 'Season Position'
        }
    else:
        display_columns = ['driverId', 'positionText', f'points_{points_chosen}', f'cumulative_points_{points_chosen}', 'driver_position']
        column_names = {
            'driverId': 'Driver',
            'positionText': 'Race Position',
            f'points_{points_chosen}': 'Race Points',
            f'cumulative_points_{points_chosen}': 'Season Points',
            'driver_position': 'Season Position'
        }

    race_results['driver_position'] = race_results[f'cumulative_points_{points_chosen}_fastest_lap' if use_bonus else f'cumulative_points_{points_chosen}'].rank(ascending=False, method='min')
    standings_df = race_results[display_columns].rename(columns=column_names)

    col.subheader(f"Standings with {points_chosen}")
    if display_race_or_year:
        standings_df_sorted = standings_df[['Driver', 'Season Position', 'Season Points']].sort_values(by='Season Points', ascending=False)
    else:
        standings_df_sorted = standings_df[['Driver', 'Race Position', 'Race Points']].sort_values(by='Race Points', ascending=False)
    col.dataframe(standings_df_sorted, use_container_width=True, hide_index=True)


# Get DataFrames from st.session_state
session_data = get_session_state_data(['grands_prix', 'races', 'circuits', 'races_results', 'points_systems', 'selected_gp', 'annee_selectionnee', 'gp_details', 'gp_races', 'circuit_id', 'circuit_details', 'driver_standings', 'pilotes_annee'])

sidebar_filters(session_data['races'], session_data['grands_prix'], session_data['circuits'], session_data['driver_standings'])

session_data = get_session_state_data(['grands_prix', 'races', 'circuits', 'races_results', 'points_systems', 'selected_gp', 'annee_selectionnee', 'gp_details', 'gp_races', 'circuit_id', 'circuit_details', 'driver_standings', 'pilotes_annee'])

if not session_data['selected_gp'] or not session_data['annee_selectionnee']:
    st.info("🚦 Please select a Grand Prix to display details!")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**🏆 Date:** {session_data['gp_races'].iloc[0]['date']}")
        st.markdown(f"**🏆 GP Name:** {session_data['gp_details']['fullName']}")
        st.markdown(f"**🏆 Race Name:** {session_data['gp_races'].iloc[0]['officialName']}")
        st.markdown(f"**🏟️ Circuit Name:** {session_data['circuit_details']['fullName']}")
        st.markdown(f"**📍 Location:** {session_data['circuit_details']['placeName']}")

    with col2:
        st.markdown(f"**🔤 Abbreviation:** {session_data['gp_details']['abbreviation']}")
        st.markdown(f"**🛣️ Circuit Type:** {session_data['circuit_details']['type']}")
        st.markdown(f"**🌍 Country:** {session_data['gp_details']['countryId']}")
        st.markdown(f"**🏎️ Total Races Held:** {session_data['circuit_details']['totalRacesHeld']}")
        st.markdown(f"**📏 Circuit Length:** {session_data['gp_races'].iloc[0]['courseLength']} km")

    st.markdown("---")

# Apply function to race results
st.session_state['races_results'] = calculate_scores(session_data['races_results'], session_data['points_systems'], session_data['pilotes_annee'])

# Get results for selected race
selected_race = session_data['gp_races'][session_data['gp_races']['year'] == session_data['annee_selectionnee']].iloc[0] if session_data['gp_races'] is not None else None
race_results = session_data['races_results'][
    (session_data['races_results']['raceId'] == selected_race['id']) &
    (session_data['races_results']['year'] == session_data['annee_selectionnee'])
]

# Display driver standings
st.subheader(f"Driver standings for {session_data['selected_gp']} {session_data['annee_selectionnee']}")

# Add button to choose between position and points display
display_race_or_year = st.selectbox("Season or race results", options=[True, False], format_func=lambda x: "Season" if x else "Race", index=0)

# Allow user to choose two points systems for comparison
col1, col2 = st.columns(2)
points_systems = [col.split('_', 1)[1] for col in race_results.columns if col.startswith('points_') and not col.startswith('points_cumules_') and not col.endswith('_fastest_lap')]

with col1:
    points_chosen_1 = st.selectbox("Choose first points system", points_systems, key='points_chosen_1', index=0)
    use_bonus_1 = st.checkbox("Include bonus point for fastest lap", value=True, key='use_bonus_1')
with col2:
    points_chosen_2 = st.selectbox("Choose second points system", points_systems, key='points_chosen_2', index=1)
    use_bonus_2 = st.checkbox("Include bonus point for fastest lap", value=True, key='use_bonus_2')

# Display tables side by side
display_standings(race_results, points_chosen_1, use_bonus_1, col1)
display_standings(race_results, points_chosen_2, use_bonus_2, col2)
