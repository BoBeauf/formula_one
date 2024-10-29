import streamlit as st
import pandas as pd
import pydeck as pdk
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data

# Page configuration
st.set_page_config(page_title="Race Map by Season", layout="wide")

# Page title
st.title("Race Map by Season")

# Get DataFrames from st.session_state
session_data = get_session_state_data(['races', 'circuits', 'grands_prix'])

# Selector to choose a specific year
available_years = sorted(session_data['races']['year'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Choose a year", available_years, index=0)
st.session_state['annee_selectionnee_index'] = available_years.index(selected_year)

# Filter races for selected year
year_races = session_data['races'][session_data['races']['year'] == selected_year]

# Get circuit details for races of selected year
year_circuits = session_data['circuits'][session_data['circuits']['id'].isin(year_races['circuitId'].unique())]


# Define colors for pins with gradient from yellow to red
def set_color(index, total):
    ratio = index / (total - 1)
    red = int(255 * ratio)
    yellow = int(255 * (1 - ratio))
    return [red, yellow, 0, 160]

# Sort races by date
year_races_sorted = year_races.sort_values(by='date')
year_circuits['color'] = [set_color(i, len(year_circuits)) for i in range(len(year_circuits))]
line_data = pd.merge(year_races_sorted, year_circuits, left_on='circuitId', right_on='id')

# Create map with pydeck
scatterplot_layer = pdk.Layer(
    'ScatterplotLayer',
    data=line_data,  # Use line_data to include race information
    get_position='[longitude, latitude]',
    get_radius=150000,  # Increase pin size
    get_color='color',  # Use defined color
    pickable=True
)

# Create lines between circuits using positions of successive races
line_data['source_longitude'] = line_data['longitude'].shift()
line_data['source_latitude'] = line_data['latitude'].shift()
line_data = line_data.dropna(subset=['source_longitude', 'source_latitude'])

line_layer = pdk.Layer(
    'LineLayer',
    data=line_data,
    get_source_position='[source_longitude, source_latitude]',
    get_target_position='[longitude, latitude]',
    get_color='[128, 128, 128, 160]',  # Gray color for lines
    get_width=1
)

view_state = pdk.ViewState(
    latitude=year_circuits['latitude'].mean(),
    longitude=year_circuits['longitude'].mean(),
    zoom=2,
    pitch=0
)

r = pdk.Deck(
    layers=[scatterplot_layer, line_layer],
    initial_view_state=view_state,
    tooltip={"text": "Race {round}: {name}"},  # Display race number
    map_style='light'  # Black map
)

st.pydeck_chart(r)
