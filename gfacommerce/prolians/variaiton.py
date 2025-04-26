import requests
from   bs4 import BeautifulSoup

def getGallery(soup):
    imgList = []
    try:
        gallery           = soup.select(".product-image")

        for img in gallery:
            img  = img.get('src').replace('11e08f74e5ceca7d26cfe2217400925b', 'a70b94d2a14edc0fdfd5ffbe8a490921')
            imgList.append(img)
        
        imgList = ",".join(imgList)
    except:

        imgList = ''

    return imgList


def getReference(url):
    
    html =  requests.get(url)
    soup =  BeautifulSoup(html.text, 'html.parser')
    ref  =  soup.select_one("[data-testid='produit-reference-fabricant']")

    return ref.text

def setGallerySoup(url):

    res  =  requests.get(url)
    soup =  BeautifulSoup(res.text, 'html.parser')

    data = getGallery(soup)

    return data

def getVariation(soup, produitID):

    allVariation = []

    variation = soup.select_one(".dc__reference_table_table")
    if not variation:
        print("Aucune table de variation trouvée.")
        return None

    variation_thead = variation.select('thead th')
    headers = [th.text.strip() for th in variation_thead] 
  
    variation_body = variation.select('tbody tr')

    for tr in variation_body:
        tds = tr.select('td') 
        variation_data = {
            "attributes": {}  
        }

        for index, header in enumerate(headers):
            if index >= len(tds):
                variation_data[header] = "N/A"
                continue

            td = tds[index]

            variation_data['parentID'] = produitID
         
            if header == "Références":
           
                name_link = td.select_one(".productName a")

                if name_link:
                    variation_data["variation_link"]  = name_link['href']
                    reference = getReference(name_link['href'])
                    variation_data['variation_ref']   = reference

                tooltip = td.select_one(".info-tooltip_content")
                if tooltip:
                    tooltip_text = tooltip.text.strip()  
                    if ":" in tooltip_text:
                        attr_name, attr_value = [part.strip() for part in tooltip_text.split(":", 1)]
                        variation_data["attributes"][attr_name] = attr_value

            elif header == "Prix":
           
                price = td.select_one(".current-product-price")
                variation_data["variation_prix"] = price.text.strip() if price else "N/A"

            else:
                variation_data["attributes"][header] = td.text.strip()
              
        allVariation.append(variation_data)

    return allVariation

