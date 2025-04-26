import pandas as pd
import os

# Définir le nom de fichier et le chemin
file = "abus-variation.xlsx"
path = os.path.join('../prolians', file)

# Charger le fichier Excel
excel = pd.read_excel(path)

# Parcourir les lignes du DataFrame
for index, row in excel.iterrows():
    attr = row.get('Attributes', '')
    
    if pd.isna(attr):
        continue  # Ignorer les lignes où 'Attributes' est vide ou NaN

    attr_array = attr.split(',')

    
    if index == 0:
        print(attr_array)
