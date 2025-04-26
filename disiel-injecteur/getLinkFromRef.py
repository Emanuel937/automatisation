import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_product_data(reference, cache):
    if reference in cache:
        return cache[reference]  # Retourner les données en cache si déjà récupérées
    
    url = f'https://www.autonorma.fr/tous-les-produits/?q={reference}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    card = soup.select_one("div.strip-card.strip-right")  # Sélection du premier produit trouvé
    if not card:
        return None  # Retourne None si aucun produit n'est trouvé
    
    title = card.select_one("a[class='name']").text.strip()
    price = card.select_one("p[class='total-price']").text.strip()
    link = "https://www.autonorma.fr" + card.select_one("a[class='name']").get('href')
    
    product_data = {
        "title": title,
        "price": price,
        "link": link,
        "code_moteur": '',
        "brand": '',
        "brand_html": '',
        "description": ''
    }
    
    cache[reference] = product_data  # Stocker les données dans le cache
    return product_data

# Charger le fichier Excel contenant les références
file_path = "site_code_moteur_vide.xlsx"  # Modifier avec le chemin correct
output_file = "other.xlsx"
df = pd.read_excel(file_path)

# Vérifier si la colonne de référence existe
if "reference" not in df.columns:
    raise ValueError("Le fichier Excel doit contenir une colonne nommée 'reference'.")

data = []
total = 0
cache = {}  # Dictionnaire pour stocker les résultats déjà récupérés

for ref in df["reference"].dropna():
    product_data = fetch_product_data(ref, cache)
    if product_data:
        total += 1
        print(f'Traitement de la référence {ref} - Total récupéré : {total}')
        product_data["reference"] = ref  # Ajouter la référence aux données collectées
        data.append(product_data)
    else:
        print(f'Aucun produit trouvé pour la référence {ref}')

# Créer un DataFrame avec les nouvelles données et fusionner avec l'existant
df_new = pd.DataFrame(data)
df_merged = df.merge(df_new, on="reference", how="left")

# Enregistrer les données mises à jour dans un fichier Excel
df_merged.to_excel(output_file, index=False)

print(f"Les données ont été enregistrées dans le fichier {output_file}.")
