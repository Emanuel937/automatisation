import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

file   = "BOSCH.csv"
brand  = 'BOSCH'
path   =  os.path.join(file)
df     =  pd.read_csv(path)

df     = df[~pd.isna(df['imgCover'])]


df.to_csv(file, index=False)
"""
df['BRAND'] = brand

start = 0

def getGallery(soup):

    global start

    imgList = []

    try:
        gallery = soup.select(".product-image")

        for img in gallery:

            img_src = img.get('src')
            print("------------")
          

            if img_src:
                # Remplacement du hash si nécessaire
                img_src = img_src.replace('11e08f74e5ceca7d26cfe2217400925b', 'a70b94d2a14edc0fdfd5ffbe8a490921')
                imgList.append(img_src)
               
            if start >= 0:
                start += 1 

       
        return ",".join(imgList[:-1] if len(imgList) > 1 else imgList)
    
    
    except Exception as e:

        print(f"Erreur lors du parsing : {e}")
        return ""

for index, row in df.iterrows():
    
    product_url = row['link']
    img         = df.at[index, 'imgCover'] 

    if   not pd.isna(img):
            continue
    
    try:

        html    = requests.get(product_url, timeout=10)
        soup    = BeautifulSoup(html.text, 'html.parser')
       
        new_img = getGallery(soup)

        df.at[index, 'imgCover'] = new_img

        print('index:', index, 'old value:', img)
        print( 'new value is :', new_img, 'url', row['link'] )

    except Exception as e:
        print(f"Erreur avec l'URL {product_url} : {e}")
        df.at[index, 'link'] = ''

# Sauvegarde dans le même fichier
df.to_csv(file, index=False)
"""