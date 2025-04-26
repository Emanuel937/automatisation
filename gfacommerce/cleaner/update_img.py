import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

file = "BOSCH.xlsx"
brand = 'BOSCH'
path = os.path.join( file)
df = pd.read_excel(path)
df['BRAND'] = brand

start = 0
def getGallery(soup):

    global start

    imgList = []
    try:
        gallery = soup.select(".product-image")
        for img in gallery:
            img_src = img.get('src')
            if img_src:
                # Remplacement du hash si nécessaire
                img_src = img_src.replace('11e08f74e5ceca7d26cfe2217400925b', 'a70b94d2a14edc0fdfd5ffbe8a490921')
                imgList.append(img_src)

            if start == 0:
                #print(imgList)
                start += 1 

        imgList = imgList[:-1]  # Retire la dernière image si besoin

        return ",".join(imgList)
    except Exception as e:
        print(f"Erreur lors du parsing : {e}")
        return ""

# Mise à jour des données
for index, row in df.iterrows():
    product_url = row['link']
    try:
        html = requests.get(product_url, timeout=10)
        soup = BeautifulSoup(html.text, 'html.parser')
        new_img = getGallery(soup)
        df.at[index, 'imgCover'] = new_img
        if index == 0:
             print(new_img)

    except Exception as e:
        print(f"Erreur avec l'URL {product_url} : {e}")
        df.at[index, 'link'] = ''

# Sauvegarde dans le même fichier
df.to_csv(file, index=False)
