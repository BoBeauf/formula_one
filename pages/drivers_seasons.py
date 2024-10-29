import streamlit as st
import pandas as pd
import altair as alt
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data

# Page configuration
st.set_page_config(page_title="Driver Evolution by Season", layout="wide")

# Get DataFrames from st.session_state
session_data = get_session_state_data(['driver_standings', 'seasons_entrants_driver'])

# Add constructorId and rounds to session_data['driver_standings'] by applying selection rules
def select_constructor(group):
    # Sort by number of rounds (descending) then by lowest round (ascending)
    group = group.sort_values(by=['rounds', 'roundsText'], ascending=[False, True])
    return group.iloc[0]

# Apply selection function for each group of drivers by year
selected_entrants = session_data['seasons_entrants_driver'].groupby(['year', 'driverId']).apply(select_constructor).reset_index(drop=True)

# Merge selected data with driver_standings
session_data['driver_standings'] = session_data['driver_standings'].merge(
    selected_entrants[['year', 'driverId', 'constructorId', 'rounds']],
    on=['year', 'driverId'],
    how='left'
)

# Page title
st.title("Driver Evolution by Season")

# Allow user to select drivers
available_drivers = session_data['driver_standings']['driverId'].unique()
selected_drivers = st.multiselect("Select drivers to display", available_drivers)

# Filter data for selected drivers
selected_drivers_standings = session_data['driver_standings'][session_data['driver_standings']['driverId'].isin(selected_drivers)]

st.markdown("### 🏆 Driver Championship Positions")

if not selected_drivers_standings.empty:
    # Prepare data for Altair
    data_chart = selected_drivers_standings.pivot(index='year', columns='driverId', values='positionDisplayOrder').reset_index().melt('year', var_name='Driver', value_name='Position')

    # Add constructor information
    data_chart = data_chart.merge(
        session_data['driver_standings'][['year', 'driverId', 'constructorId']],
        left_on=['year', 'Driver'],
        right_on=['year', 'driverId'],
        how='left'
    )

    # Create chart with Altair
    chart = alt.Chart(data_chart).mark_line(point=True).encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y('Position:Q', title='Position', scale=alt.Scale(reverse=True)),
        color='Driver:N',
        tooltip=['year:O', 'Driver:N', 'Position:Q', 'constructorId:N']
    ).properties(
        width=800,
        height=400
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Please select at least one driver to display the chart.")

st.markdown("### 🚗 Driver Teams")

if not selected_drivers_standings.empty:
    # Prepare data for second chart
    data_chart_teams = selected_drivers_standings.pivot(index='year', columns='driverId', values='constructorId').reset_index().melt('year', var_name='Driver', value_name='Team')

    # Create second chart with Altair to show team changes
    chart_teams = alt.Chart(data_chart_teams).mark_line(point=True).encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y('Team:N', title='Team'),
        color='Driver:N',
        tooltip=['year:O', 'Driver:N', 'Team:N']
    ).properties(
        width=800,
        height=400
    ).interactive()

    st.altair_chart(chart_teams, use_container_width=True)
else:
    st.info("Please select at least one driver to display the team changes chart.")
