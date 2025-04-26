import pandas as pd
import os

file = "upower.xlsx"
path = os.path.join(file)

df = pd.read_excel(path)

# Supprimer les lignes où une colonne quelconque est vide
df = df.dropna(how='any')

# Sauvegarder le fichier nettoyé
df.to_excel(file, index=False)
