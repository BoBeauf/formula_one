import streamlit as st
import pandas as pd
import plotly.express as px
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data, get_constructor_standings_data, get_constructor_drivers_data

# Page configuration
st.set_page_config(page_title="Teams Tracking", layout="wide")

# Page title
st.title("Teams Tracking")

# Get DataFrames from st.session_state
session_data = get_session_state_data(['constructors', 'constructors_chronology', 'seasons_constructors_standings', 'engine_manufacturers', 'seasons_entrants_driver', 'drivers'])

# Data preparation
df_constructors = session_data['constructors']
df_chronology = session_data['constructors_chronology']
df_season_standings = session_data['seasons_constructors_standings']
df_engine_manufacturers = session_data['engine_manufacturers']
df_seasons_entrants_driver = session_data['seasons_entrants_driver']
df_drivers = session_data['drivers']

# Add filter to select multiple constructors
selected_constructors = st.multiselect(
    "Select one or more constructors",
    options=sorted(df_constructors['fullName'].unique().tolist())
)

if not selected_constructors:
    st.warning("🚦 Please select at least one team.")
else:
    # Initialize empty DataFrames to store results
    df_all_constructors = pd.DataFrame()
    df_all_constructors_drivers = pd.DataFrame()

    # Call function for each selected constructor
    for constructor in selected_constructors:
        df_constructor_standings = get_constructor_standings_data(constructor, df_constructors, df_chronology, df_season_standings, df_engine_manufacturers, df_seasons_entrants_driver)
        df_all_constructors = pd.concat([df_all_constructors, df_constructor_standings])
    
    for constructor in selected_constructors:
        df_constructor_drivers = get_constructor_drivers_data(constructor, df_constructors, df_chronology, df_seasons_entrants_driver, df_drivers)
        df_all_constructors_drivers = pd.concat([df_all_constructors_drivers, df_constructor_drivers])

    # Prepare data for the chart
    df_graph = df_all_constructors.sort_values(['id_constructeur', 'year'])

    # Merge df_graph with df_all_constructors_drivers to get driver information
    df_graph = pd.merge(df_graph, df_all_constructors_drivers[['year', 'id_constructeur', 'driverName']], 
                        on=['year', 'id_constructeur'], how='left')

    # Group drivers by year and constructor
    df_graph['drivers'] = df_graph.groupby(['year', 'id_constructeur'])['driverName'].transform(lambda x: ', '.join(x.dropna().unique()))

    # Create chart
    fig = px.line(df_graph, x='year', y='positionNumber', color='id_constructeur',
                  title="Evolution of constructor positions over the years",
                  labels={'year': 'Year', 'positionNumber': 'Position', 'constructorName': 'Constructor', 'id_constructeur': 'Team'},
                  markers=True,
                  hover_data=['constructorName', 'engineManufacturerName', 'points', 'drivers'])

    # Reverse y-axis so best position (1) is at the top
    fig.update_yaxes(autorange="reversed")

    # Customize toolbox
    fig.update_traces(
        hovertemplate="<b><i>%{customdata[0]}</i></b><br>" +
                      "<b>Year</b>: %{x}<br>" +
                      "<b>Position</b>: %{y}<br>" +
                      "<b>Engine Manufacturer</b>: %{customdata[1]}<br>" +
                      "<b>Points</b>: %{customdata[2]}<br>" +
                      "<b>Drivers</b>: %{customdata[3]}<extra></extra>"
    )

    # Display chart
    st.plotly_chart(fig)

    # Create drivers table for each team
    st.markdown("### 👨‍🚀 Drivers by Team")

    # Create list of constructor pairs
    constructor_pairs = [selected_constructors[i:i+2] for i in range(0, len(selected_constructors), 2)]
    
    for pair in constructor_pairs:
        cols = st.columns(2)
        
        for i, constructor in enumerate(pair):
            with cols[i]:
                st.subheader(f"Drivers for {constructor}")
                
                # Filter data for current constructor
                df_constructor = df_all_constructors_drivers[df_all_constructors_drivers['id_constructeur'] == constructor]
                
                # Display table
                st.dataframe(df_constructor[['year', 'driverName', 'testDriver']].set_index('year'), use_container_width=True)
        
        st.markdown("---")