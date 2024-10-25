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