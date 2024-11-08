import streamlit as st
import pandas as pd
import plotly.express as px
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data, get_driver_standings_data

# Page configuration
st.set_page_config(page_title="Driver Evolution by Season", layout="wide")

# Get DataFrames from st.session_state
session_data = get_session_state_data(['driver_standings', 'seasons_entrants_driver', 'races_results', 'qualifying_results', 'drivers', 'constructors'])

# Add constructorId and rounds to session_data['driver_standings'] by applying selection rules
def select_constructor(group):
    # Sort by number of rounds (descending) then by lowest round (ascending)
    group = group.sort_values(by=['rounds', 'roundsText'], ascending=[False, True])
    return group.iloc[0]

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

# Create two columns for filters
col1, col2 = st.columns(2)

with col1:
    # Create a mapping of driver IDs to full names
    driver_names = pd.Series(
        session_data['drivers'].set_index('id')['fullName']
    ).to_dict()
    
    # Create options with real names but keep IDs as values
    selected_drivers = st.multiselect(
        "Select drivers to display",
        options=available_drivers,
        format_func=lambda x: driver_names.get(x, x)
    )

# Add dropdown for y-axis selection in second column
with col2:
    y_axis_option = st.selectbox(   
        "Select the metric to display",
        options=['championship_position', 'victories', 'podiums', 'pole_positions', 'best_position', 'best_qualif_position', 'dnfs'],
        format_func=lambda x: {
            'championship_position': 'Championship Position',
            'victories': 'Race Victories',
            'podiums': 'Podium Finishes',
            'pole_positions': 'Pole Positions', 
            'best_position': 'Best Race Position',
            'best_qualif_position': 'Best Qualifying Position',
            'dnfs': 'DNFs'
        }[x]
    )

if not selected_drivers:
    st.warning("🚦 Please select at least one driver.")

else:
    df_all_drivers_standings = pd.DataFrame()
    for driver in selected_drivers:
        df_driver_standings = get_driver_standings_data(driver, session_data['races_results'], session_data['qualifying_results'], session_data['drivers'], session_data['driver_standings'])
        df_all_drivers_standings = pd.concat([df_all_drivers_standings, df_driver_standings])

    # Add constructor information to df_all_drivers_standings
    df_all_drivers_standings = df_all_drivers_standings.merge(
        session_data['seasons_entrants_driver'][['year', 'driverId', 'constructorId']],
        on=['year', 'driverId'],
        how='left'
    )

    # Add constructor name
    df_all_drivers_standings = df_all_drivers_standings.merge(
        session_data['constructors'][['id', 'name']],
        left_on='constructorId',
        right_on='id',
        how='left'
    ).rename(columns={'name': 'constructorName'})

    st.markdown("### 🏆 Driver Championship Positions")
    
    # Drop duplicates before pivoting to avoid index issues
    df_for_pivot = df_all_drivers_standings.drop_duplicates(['year', 'driverName'])
    
    # Prepare data for plotly
    data_chart = df_for_pivot.pivot(index='year', columns='driverName', values=y_axis_option).reset_index().melt('year', var_name='Driver', value_name='Value')

    # Add constructor information
    data_chart = data_chart.merge(
        df_all_drivers_standings[['year', 'driverName', 'constructorName']].drop_duplicates(['year', 'driverName']),
        left_on=['year', 'Driver'],
        right_on=['year', 'driverName'],
        how='left'
    )

    # Create chart with plotly
    fig = px.line(data_chart, x='year', y='Value', color='Driver',
                  title=f"Evolution of Driver {y_axis_option.replace('_', ' ').title()}",
                  labels={'year': 'Year', 'Value': y_axis_option.replace('_', ' ').title(), 'Driver': 'Driver'},
                  markers=True,
                  hover_data=['Driver', 'constructorName'],
                  height=500)
    
    # Reverse y-axis if showing positions
    if y_axis_option in ['championship_position', 'best_position', 'best_qualif_position']:
        fig.update_layout(yaxis={'autorange': 'reversed'})

    # Customize toolbox
    fig.update_traces(
        hovertemplate="<b><i>%{customdata[0]}</i></b><br>" +
                      "<b>Year</b>: %{x}<br>" +
                      "<b>Metric Value</b>: %{y}<br>" +
                      "<b>Team</b>: %{customdata[1]}<extra></extra>"
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🚗 Driver Teams")

    # Prepare data for second chart
    # Drop duplicates before pivoting to avoid index issues
    data_chart_teams = df_for_pivot.pivot(index='year', columns='driverId', values='constructorName').reset_index().melt('year', var_name='Driver', value_name='Team')

    # Create second chart with plotly to show team changes
    fig_teams = px.line(data_chart_teams, x='year', y='Team', color='Driver',
                       title="Evolution of Driver Teams",
                       labels={'year': 'Year', 'Team': 'Team', 'Driver': 'Driver'},
                       markers=True,
                       hover_data=['Driver'],
                       height=500)
    
    fig_teams.update_traces(
        hovertemplate="<b><i>%{customdata[0]}</i></b><br>" +
                      "<b>Year</b>: %{x}<br>" +
                      "<b>Team</b>: %{y}<extra></extra>"
    )

    st.plotly_chart(fig_teams, use_container_width=True)