import pandas as pd
import requests
from bs4 import BeautifulSoup

def setupSoup(index):
    # Utilisation de f-string pour formater l'URL avec l'index
    url = f'https://www.autonorma.fr/c/turbocompresseurs?page={index}'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    card = soup.select("div.strip-card.strip-right")  # Sélectionner les éléments de la carte

    return card

# Liste pour stocker les données des produits
data = []

total = 0
# Boucle pour parcourir les pages de 1 à 197 (198 exclu)
for index in range(1, 430):
    card = setupSoup(index)
    for element in card:
        total += 1
        print(f'total is :', total) 
        title = element.select_one("a[class='name']").text.strip()  # Récupérer le titre
        price = element.select_one("p[class='total-price']").text.strip()  # Récupérer le prix
        link = "https://www.autonorma.fr" + element.select_one("a[class='name']").get('href')  # Récupérer le lien complet
        
        # Ajouter les informations dans la liste 'data'
        data.append({
            "title": title,
            "price": price,
            "link": link,
            'code_moteur':'',
            'brand':'',
            'brand_html':'',
            'description': ''

        })
       
# Créer un DataFrame pandas avec les données collectées
df = pd.DataFrame(data)

# Enregistrer les données dans un fichier Excel
df.to_excel("turbo_compresseur_autonorma_link.xlsx", index=False)

print("Les données ont été enregistrées dans le fichier injecteurs_autonorma.xlsx.")
