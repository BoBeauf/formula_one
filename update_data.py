import requests
import os
import zipfile
import io

# URL de l'API GitHub pour les releases
url_api_releases = 'https://api.github.com/repos/f1db/f1db/releases/tag/v2024.18.0'

# Dossier où les fichiers CSV seront stockés
dossier_csv = 'f1db-csv'

# Créer le dossier s'il n'existe pas
if not os.path.exists(dossier_csv):
    os.makedirs(dossier_csv)

# Obtenir les informations de la dernière release
response = requests.get(url_api_releases)
release_data = response.json()

# Télécharger le fichier zip contenant les CSV
for asset in release_data['assets']:
    if asset['name'] == 'f1db-csv.zip':
        print(f"Téléchargement de {asset['name']}...")
        response = requests.get(asset['browser_download_url'])
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(dossier_csv)
        print(f"{asset['name']} téléchargé et extrait avec succès.")

print("Tous les fichiers CSV ont été téléchargés et extraits.")