import pandas as pd
import requests
from bs4 import BeautifulSoup

# Charger le fichier Excel avec l'index
df = pd.read_excel('other.xlsx')


total = 0
t     = 0
# Vérifier si la colonne "index" existe
if 'index' not in df.columns:
    df['index'] = df.index  # Si elle n'existe pas, on la recrée

# Cache pour éviter les requêtes redondantes
cache = {}

# Fonction pour récupérer les données depuis l'URL
def get_product_data(url):
    global total 

    if url in cache:
        print(f"♻️ Utilisation du cache pour {url}")
        return cache[url]  # Récupération des données en cache
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Récupérer les informations
            engine_div = soup.find("div", id="engine-codes-component")
            code_moteur = ",".join([span.text.strip() for span in engine_div.find_all("span")]) if engine_div else ''

            description = soup.select_one("div[class='long-text']")
            description = description.text.strip() if description else ''

            brand_html = soup.select_one("div[id='car-brand0']")
            brand = brand_html.text.strip() if brand_html else ''

            # Stocker dans le cache
            cache[url] = (code_moteur, description, brand)
            total += 1
            print(f'Total avec code moteur', {total})
            return code_moteur, description, brand
        else:
            print(f"⚠️ Erreur HTTP {response.status_code} pour URL : {url}")
            return '', '', ''
    except requests.exceptions.RequestException as e:
        print(f"🚨 Erreur de connexion pour URL : {url} - {e}")
        return '', '', ''

# Boucle sur chaque ligne et mise à jour des données
for index, row in df.iterrows():
    url = row['link_y']

    if pd.isna(url) or not isinstance(url, str):
        print(f"❌ URL invalide à la ligne {index}")
        continue

    print(f"🔄 Traitement {index + 1}/{len(df)} : {url}")

    # Récupérer les nouvelles données
    code_moteur, description, brand = get_product_data(url)

    # Mettre à jour la ligne correspondante dans le dataframe
    df.at[index, 'code_moteur'] = code_moteur
    df.at[index, 'description'] = description
    df.at[index, 'brand'] = brand

# Sauvegarder dans le fichier source **SANS** modifier l'index
df.to_excel('other_cm.xlsx', index=False)
print("✅ Fichier Excel mis à jour avec succès.")
