# THIS CODE GET THE PRODUCT DATA FROM CATEGORIES PAGE 
# THE DATA ARE NAME, PRIX, COVER 

import requests
from bs4 import BeautifulSoup
from variaiton import *  # Assurez-vous que ce module existe et fonctionne
import pandas as pd
from fetcher import PlaywrightFetcher  

products           = []
variationProducts  = []
brands: str             = 'soppec'
lastPageIndex: int      = 1
startProduitID: int     =  6695

produitID  = startProduitID
fetcher    = PlaywrightFetcher()

def saveData(data, fileName):
    global brands
    df = pd.DataFrame(data)
    df.to_excel(f"{brands}-{fileName}.xlsx", index=False)

def saveVariation(data, fileName):
    all_items = []
    for item in data:
        if isinstance(item, dict):
            all_items.append(item)
        elif isinstance(item, list):
            all_items.extend(item)

    def format_item(item):
        if 'attributes' in item:
            attributes_str = ", ".join(
                f"{key}:{value}" for key, value in item['attributes'].items()
                if key not in ['Stocks', 'Ajouter au panier']
            )
        else:
            attributes_str = ""
        return {
            'Attributes': attributes_str,
            'ParentID': item.get('parentID'),
            'VariationLink': item.get('variation_link'),
            'VariationPrix': item.get('variation_prix'),
            'VariationRef': item.get('variation_ref')
        }

    df = pd.DataFrame([format_item(item) for item in all_items])
    file_path = f"{brands}-{fileName}.xlsx"
    df.to_excel(file_path, index=False)

def tryExcept(soup, selector):
    try:
        result = soup.select_one(selector).text
    except Exception:
        result = ' '
    return result

def tryExceptHTML(soup, selector):
    try:
        result = soup.select_one(selector)
    except Exception:
        result = ' '
    return result  # Note : ici, vous ne retourniez rien dans le code original

def getProductExtraData(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    imgList = []

    ref = tryExcept(soup, "[data-testid='produit-reference-fabricant']")
    description = tryExcept(soup, '.dc_content.dc__description')
    techniqueDetails = tryExceptHTML(soup, "[data-testid='produit-caracteristique']")
    variation = getVariation(soup, produitID)  # Assurez-vous que cette fonction existe
    imgList = getGallery(soup)  # Assurez-vous que cette fonction existe

    data = {
        'ref': ref,
        'description': description,
        'techniqueDetails': techniqueDetails,
        'gallery': imgList,
    }
    
    variationProducts.append(variation)
    return data

def init(brands, pageIndex):
    global products, produitID, fetcher

    url = f'https://www.prolians.fr/nos-marques/{brands}/?productPage={pageIndex}&q='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    itens = soup.select('.dc__product_slot')

    for item in itens:
        name = item.select_one('.dc__product_slot__name').text
        prix = item.select_one('.dc__product_slot__price__amount').text
        link = item.select_one('.dc__product_slot__main_link').get('href')
        imgCover = item.select_one('.product-image-photo').get('src')

        extraData = getProductExtraData(link)
        produitID += 1

        # Récupérer les catégories avec Selenium
        categories_html = fetcher.fetch_html(link, "ul.items")
        categories = []
        if categories_html:  # Vérifier si le HTML est valide
            categories_soup = BeautifulSoup(categories_html, 'html.parser')
            categories = [category.text for category in categories_soup.select('.item.category')]
            categories = categories[1:] if len(categories) > 1 else categories
        categories = ",".join(categories) if categories else "Non trouvé"

        data = {
            'produitID': produitID,
            'name': name,
            'prix': prix,
            'link': link,
            'imgCover': imgCover,
            'reference': extraData['ref'],
            'description': extraData['description'],
            'techniqueDetails': extraData['techniqueDetails'],
            'category': categories
        }
       
        products.append(data)

    return products

def run():
    global products, variationProducts, produitID
    
    for pageIndex in range(1, lastPageIndex + 1):  
        print('Page n°:', pageIndex)
        init(brands, pageIndex)
   
    saveData(products, "products")
    saveVariation(variationProducts, "variation")
    print("Données sauvegardées avec succès")
    print("Last produits id:", produitID)

if __name__ == "__main__":
    try:
        run()
    finally:
        fetcher.close() 



