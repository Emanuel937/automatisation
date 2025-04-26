import requests
import pandas as pd
from typing import Optional, List, Dict
from bs4 import BeautifulSoup, Tag

def get_element_text(element: Optional[Tag]) -> str:
    return element.text.strip() if element else "Nom inconnu"

def clean_empty_tags(soup: BeautifulSoup) -> BeautifulSoup:
    for tag in soup.find_all():
        if tag.name in ['br', 'img']:
            continue
        if not tag.text.strip() and not tag.find('img'):
            tag.decompose()
        if tag.name == "u" and tag.parent.name == "u":
            tag.unwrap()
    return soup

class OtherDetails:
    soup: BeautifulSoup

    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup
       

    def description(self) -> str:
        try:
            description = clean_empty_tags(self.soup.select('.acLists')[0])
            return description
        except IndexError:
            return "Pas de description"

    def code_ean(self) -> str:
        try:
            code_ean = self.soup.select_one('label.label span')
            return get_element_text(code_ean).split(']')[0]
        except (IndexError, AttributeError):
            return "EAN non trouvé"

    def reference(self) -> str:

        reference = self.soup.select_one('.label span')
        return get_element_text(reference)
    
    
    def getAttributes(self)->None:

        try:
            attributes =  self.soup.select_one('.form-control-label')
            attributes = attributes.text.split(':')
            attributes = attributes[0]  

        except Exception as error:
            attributes = None

        return attributes

    def attributesValues(self):

        try:
            values =  [ data.text for data in self.soup.select(".form-control-select option")]
            values = ",".join(values)
        except Exception as erro:
            values = " "
        return values


    def fiche_technique(self) -> str:
        try:
            tech_details = clean_empty_tags(self.soup.select('.acLists')[1])
            return tech_details
        except IndexError:
            return " "
        
    def categories(self)->str:
        try:
            category =  [data.text.strip() for data in self.soup.select(".breadcrumb ol li")]
            category = category[1:]
            category = ','.join(category)

          
        except Exception as error:
            category =  " "
        return category
    

class IDF(OtherDetails):
    url: str = ""
    last_index_page: int
    products: List[Dict[str, Optional[str]]] = []  # Typage explicite
    total: int = 0

    def __init__(self, brand: str) -> None:
        self.brand = brand
        self.url = f"https://www.ifd-outillage.fr/{brand}"
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, "html.parser")
            super().__init__(self.soup)
        except requests.RequestException as e:
            raise ValueError(f"Erreur lors de la récupération de l’URL {self.url}: {e}")

    def product_name(self, catalog: Tag) -> str:
        product_element = catalog.select_one('.h3.product-title')
        return get_element_text(product_element)

    def product_single_page(self, catalog: Tag) -> Optional[Dict[str, str]]:
        link_element = catalog.find("a")
        url = link_element["href"] if link_element and "href" in link_element.attrs else None

        if url:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                details_product_soup = BeautifulSoup(response.text, "html.parser")
                details = OtherDetails(details_product_soup)
                return {
                    "Ref"                  : details.reference(),
                    "Des"                  : details.description(),
                    "Eean"                 : details.code_ean(),
                    "Fiche"                : details.fiche_technique(),
                    "Url"                  : url,
                    "attr":  f'{details.getAttributes()}: {details.attributesValues()}',
                    'categories': details.categories()
                }
            except requests.RequestException as e:
                print(f"Erreur lors de la récupération de la page produit {url}: {e}")
                return None
        return None

    def product_cover_image(self, catalog: Tag) -> str:
        cover_image = catalog.select_one('.thumbnail-container .img-fluid.product-thumbnail-first')
        return cover_image.get('data-original', "Image non trouvée") if cover_image else "Image non trouvée"

    def get_catalogues_product(self) -> None:  # Changement de type de retour
        catalog_list = self.soup.find_all("div", class_="js-product-miniature-wrapper")

        for product in catalog_list:
            name = self.product_name(product)
            details = self.product_single_page(product)
            image = self.product_cover_image(product)

            product_info = {
                "Nom"        : name,
                "Reférence"   : details["Ref"] if details else "Non trouvé",
                "Code_EAN"   : details["Eean"] if details else "Non trouvé",
                "Description": details["Des"] if details else "Non trouvé",
                "Fiche"      : details["Fiche"] if details else "Non trouvé",
                "Image"      : image,
                "Url"        : details['Url'],
                "attr"       : details['attr'],
                'categories' : details['categories']
            }

         

            self.products.append(product_info)
            self.total += 1
            print(f'total: {self.total}; Reference: {details["Ref"] if details else "Non trouvé"}')

    @classmethod
    def main(cls, brand: str, last_index_page:int) -> None:
        
        cls.last_index_page = last_index_page

        instance = cls(brand) 
        for current_index in range(1, cls.last_index_page + 1):
            print(f"--------current page index: {current_index}")
            url = f"https://www.ifd-outillage.fr/{brand}?page={current_index}"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                instance.soup = BeautifulSoup(response.text, "html.parser")
                instance.get_catalogues_product()
            except requests.RequestException as e:
                print(f"Erreur sur la page {url}: {e}")
                continue
        
        if instance.products:  # Sauvegarde seulement si des produits existent
            df = pd.DataFrame(instance.products)
            df.to_excel(f"{brand}.xlsx", index=False)
        print(f"Traitement terminé ! Total de produits: {instance.total}")

if __name__ == "__main__":
    IDF.main('stanley', 19)