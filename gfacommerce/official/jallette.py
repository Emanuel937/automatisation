import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os

# Étape 1 : Ajouter les colonnes 'img' et 'index' au fichier Excel
def extract_image_url(reference, base_url="https://www.jallatte.fr"):
    url = f"{base_url}/article.php?code={reference}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
      
        img = soup.select_one('.portfolio-thumb img')
        img_url = urljoin(base_url, img.get('src')) if img else ""
        return img_url
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de l'image pour {reference}: {e}")
        return ""

def update_excel_with_images_and_index(excel_file, output_file):
    try:
        # Charger le fichier Excel
        df = pd.read_excel(excel_file)

        # Vérifier si la colonne 'CODE' existe
        if 'CODE' not in df.columns:
            raise KeyError("La colonne 'CODE' n'existe pas dans le fichier Excel. Vérifiez les noms des colonnes.")

        # Ajouter la colonne 'img' en utilisant 'CODE' pour récupérer les URLs des images
        df['img'] = df['CODE'].apply(extract_image_url)
    
        # Ajouter la colonne 'index' commençant par 10000
        df['index'] = range(10000, 10000 + len(df))
    
        # Sauvegarder le fichier mis à jour
        df.to_excel(output_file, index=False)
        print(f"Fichier Excel mis à jour sauvegardé sous : {output_file}")
        return output_file
    except Exception as e:
        print(f"Erreur lors de la mise à jour du fichier Excel : {e}")
        return None

# Étape 2 : Générer le fichier CSV pour les déclinaisons
def generate_variants_from_excel(excel_file, csv_file):
    try:
        # Charger le fichier Excel mis à jour
        df = pd.read_excel(excel_file)
 
        # Vérifier les colonnes nécessaires
        required_columns = ['CODE', 'DESIGNATION', 'Prix Public HT', 'img', 'index', 'POINTURE']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise KeyError(f"Colonnes manquantes dans le fichier Excel : {missing_columns}")

        variants = []
        size_group_id = "1"  # ID du groupe d'attributs pour la taille dans PrestaShop
    
        for _, row in df.iterrows():
            # Utiliser 'CODE' pour la référence du produit
            reference = str(row['CODE']).strip()
            # Utiliser 'DESIGNATION' pour le nom du produit
            name = str(row['DESIGNATION']).strip()
            # Utiliser 'Prix HT Remisé' pour le prix
            price = float(str(row['Prix Public HT']).replace(' €', '').replace(',', '.'))
            # Utiliser 'img' pour l'URL de l'image
            img_url = str(row['img']).strip()
            # Utiliser 'index' pour l'ID du produit
            product_index = int(row['index'])
        
            # Extraire les tailles à partir de 'POINTURE'
            size_range = str(row['POINTURE']).split('-')
            if len(size_range) != 2:
                print(f"Format de pointure invalide pour {reference}: {row['POINTURE']}")
                continue
            try:
                sizes = list(range(int(size_range[0]), int(size_range[1]) + 1))
            except ValueError as e:
                print(f"Erreur lors de la conversion des tailles pour {reference}: {e}")
                continue
        
            # Générer une déclinaison pour chaque taille
            for size in sizes:
                variant = {
                    'index': product_index,
                    'name': name,
                    'reference': f"{reference}-{size}",
                    'price': price,
                    'image': img_url,
                    'attribute_group': "Taille",
                    'attribute_value': str(size),
                    'attribute_group_id': size_group_id
                }
                variants.append(variant)
   
        # Définir les champs du CSV
        fieldnames = [
            'ID', 'Active (0/1)', 'Name', 'Reference', 'Price tax excluded',
            'Image URL', 'Attribute 1 group', 'Attribute 1 value', 'Attribute 1 reference'
        ]

        # Écrire le fichier CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        
            for variant in variants:
                row = {
                    'ID': variant['index'],  # Utiliser l'index comme ID
                    'Active (0/1)': '1',
                    'Name': variant['name'],
                    'Reference': variant['reference'],
                    'Price tax excluded': variant['price'],
                    'Image URL': variant['image'],
                    'Attribute 1 group': variant['attribute_group'],
                    'Attribute 1 value': variant['attribute_value'],
                    'Attribute 1 reference': variant['reference']
                }
                writer.writerow(row)
    
        print(f"Fichier CSV pour les déclinaisons généré : {csv_file}")
    except Exception as e:
        print(f"Erreur lors de la génération du fichier CSV : {e}")

def main():
    # Chemins des fichiers
    excel_file = os.path.join(os.getcwd(), 'jallette.xlsx')
    updated_excel_file = "jallette_updated.xlsx"  # Fichier Excel mis à jour
    csv_file = "jallette_declinaisons.csv"  # Fichier CSV final
    
    # Vérifier si le fichier Excel existe
    if not os.path.exists(excel_file):
        print(f"Le fichier {excel_file} n'existe pas.")
        return
    
    # Étape 1 : Mettre à jour le fichier Excel avec les images et l'index
    updated_file = update_excel_with_images_and_index(excel_file, updated_excel_file)
    
    # Vérifier si l'étape 1 a réussi
    if updated_file is None:
        print("Échec de la mise à jour du fichier Excel. Arrêt du processus.")
        return
    
    # Étape 2 : Générer le fichier CSV pour les déclinaisons
    generate_variants_from_excel(updated_file, csv_file)

if __name__ == "__main__":
    main()