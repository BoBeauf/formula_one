import requests
import os

# URL de l'API GitHub pour les releases
url_api_releases = 'https://api.github.com/repos/f1db/f1db/releases/latest'

# Dossier où les fichiers CSV seront stockés
dossier_csv = 'f1db-csv'

# Créer le dossier s'il n'existe pas
if not os.path.exists(dossier_csv):
    os.makedirs(dossier_csv)

# Obtenir les informations de la dernière release
response = requests.get(url_api_releases)
release_data = response.json()

# Télécharger chaque fichier CSV
for asset in release_data['assets']:
    if asset['name'].endswith('.csv'):
        print(f"Téléchargement de {asset['name']}...")
        response = requests.get(asset['browser_download_url'])
        chemin_fichier = os.path.join(dossier_csv, asset['name'])
        with open(chemin_fichier, 'wb') as fichier:
            fichier.write(response.content)
        print(f"{asset['name']} téléchargé avec succès.")

print("Tous les fichiers CSV ont été téléchargés.")