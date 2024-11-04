    # Création d'une frise chronologique des changements
    st.subheader("Frise chronologique des changements")

    # Préparation des données pour la frise
    df_timeline = df_all_constructors.merge(df_all_constructors_drivers, on=['year', 'id_constructeur'], how='outer')
    df_timeline = df_timeline.sort_values(['id_constructeur', 'year'])

    # Création d'une frise chronologique pour chaque constructeur
    for constructeur in df_timeline['id_constructeur'].unique():
        st.subheader(f"Chronologie de {constructeur}")
        
        df_constructeur = df_timeline[df_timeline['id_constructeur'] == constructeur].sort_values('year')
        
        # Création de la frise chronologique
        items = []
        
        changes_by_year = {}
        
        for _, row in df_constructeur.iterrows():
            year = row['year']
            constructor_name = row['constructorName']
            engine = row['engineManufacturerName']
            drivers = row['driverId'].split(';') if pd.notna(row['driverId']) else []
            
            changes = []
            if _ == 0 or constructor_name != df_constructeur.iloc[_ - 1]['constructorName']:
                changes.append(f"Nom: {constructor_name}")
            if _ == 0 or engine != df_constructeur.iloc[_ - 1]['engineManufacturerName']:
                changes.append(f"Motoriste: {engine}")
            if _ == 0 or set(drivers) != set(df_constructeur.iloc[_ - 1]['driverId'].split(';')):
                changes.append(f"Pilotes: {', '.join(drivers)}")
            
            if changes:
                if year not in changes_by_year:
                    changes_by_year[year] = []
                changes_by_year[year].extend(changes)
        
        for year, changes in changes_by_year.items():
            content = " | ".join(changes)
            items.append({
                "title": str(year),
                "content": content,
                "start": f"{year}-01-01",
                "end": f"{year}-12-31",
                "icon": "🏎️"
            })
        
        timeline = st_timeline(items=items, height=400)
        
        st.write("---")



    # Création d'une frise chronologique pour chaque constructeur
    for constructeur in df_timeline['id_constructeur'].unique():
        st.subheader(f"Chronologie de {constructeur}")
        
        df_constructeur = df_timeline[df_timeline['id_constructeur'] == constructeur].sort_values('year')
        
        # Création de la frise chronologique
        items = []
        
        changes_by_year = {}
        
        for idx, row in df_constructeur.iterrows():
            year = row['year']
            constructor_name = row['constructorName']
            engine = row['engineManufacturerName']
            drivers = row['driverId'].split(';') if pd.notna(row['driverId']) else []
            
            changes = []
            if idx == 0 or constructor_name != df_constructeur.iloc[idx - 1]['constructorName']:
                changes.append({"group": "Nom", "content": constructor_name if pd.notna(constructor_name) else ""})
            if idx == 0 or engine != df_constructeur.iloc[idx - 1]['engineManufacturerName']:
                changes.append({"group": "Motoriste", "content": engine if pd.notna(engine) else ""})
            if idx == 0 or set(drivers) != set(df_constructeur.iloc[idx - 1]['driverId'].split(';') if pd.notna(df_constructeur.iloc[idx - 1]['driverId']) else []):
                changes.append({"group": "Pilotes", "content": '<br>'.join(drivers)})
            
            if changes:
                if year not in changes_by_year:
                    changes_by_year[year] = []
                changes_by_year[year].extend(changes)
        
        item_id = 1  # Initialisation d'un compteur pour générer des ID uniques
        for year, changes in changes_by_year.items():
            for change in changes:
                items.append({
                    "id": f"{year}_{change['group']}_{item_id}",
                    "title": str(year),
                    "content": change['content'],
                    "start": f"{year}-01-01",
                    "end": f"{year}-12-31",
                    "group": change['group'],
                    "icon": "🏎️"
                })
                item_id += 1  # Incrémentation du compteur
        
        timeline = st_timeline(items=items, groups=[{"id": "Nom"}, {"id": "Motoriste"}, {"id": "Pilotes"}], height=300, options={"selectable": True, 
                                                      "multiselect": True, 
                                                      "zoomable": True, 
                                                      "verticalScroll": True, 
                                                      "stack": False,
                                                      "height": 200, 
                                                      "margin": {"axis": 5}, 
                                                      "groupHeightMode": "auto", 
                                                      "orientation": {"axis": "top", "item": "top"}})
        
        st.write("---")


import streamlit as st
import pandas as pd
import plotly.express as px
from utils.sidebar import sidebar_filters
from utils.func import get_session_state_data, get_constructor_standings_data, get_constructor_drivers_data

session_data = get_session_state_data(['races_results', 'qualifying_results'])

df_races_results = session_data['races_results']
df_qualifying_results = session_data['qualifying_results']
# Create stats by constructor per year
stats_by_constructor = pd.DataFrame()

# Best result of the year
best_result = df_races_results.groupby(['year', 'constructorId'])['positionNumber'].min().reset_index(name='best_position')
stats_by_constructor = best_result

# Number of victories (position=1)
victories = df_races_results[df_races_results['positionNumber'] == 1].groupby(['year', 'constructorId']).size().reset_index(name='victories')
stats_by_constructor = pd.merge(stats_by_constructor, victories, on=['year', 'constructorId'], how='outer')

# Number of DNFs (positionText contains 'DNF')
dnfs = df_races_results[df_races_results['positionText'] == 'DNF'].groupby(['year', 'constructorId']).size().reset_index(name='dnfs')
stats_by_constructor = pd.merge(stats_by_constructor, dnfs, on=['year', 'constructorId'], how='outer')

# Number of podiums (position 1-3)
podiums = df_races_results[df_races_results['positionNumber'].isin([1,2,3])].groupby(['year', 'constructorId']).size().reset_index(name='podiums')
stats_by_constructor = pd.merge(stats_by_constructor, podiums, on=['year', 'constructorId'], how='outer')

# Best qualifying position
best_qualif = df_qualifying_results.groupby(['year', 'constructorId'])['positionNumber'].min().reset_index(name='best_qualif_position')
stats_by_constructor = pd.merge(stats_by_constructor, best_qualif, on=['year', 'constructorId'], how='outer')

# Number of pole positions (qualifying position=1)
poles = df_qualifying_results[df_qualifying_results['positionNumber'] == 1].groupby(['year', 'constructorId']).size().reset_index(name='pole_positions')
stats_by_constructor = pd.merge(stats_by_constructor, poles, on=['year', 'constructorId'], how='outer')

# Fill NaN values with 0
stats_by_constructor = stats_by_constructor.fillna(0)

# Sort values by year and victories
stats_by_constructor = stats_by_constructor.sort_values(['year', 'victories'], ascending=[True, False])

# Show data table
st.write("Constructor Statistics per Year:")
st.dataframe(stats_by_constructor)
