import os
import pandas as pd

""""
fileName   = "u-power.xlsx"
path       = os.path.join(fileName)
df         = pd.read_excel(path)



def removeTrait(x):
    # Vérifier si x est une chaîne et contient '-'
    if isinstance(x, str) and '-' in x:
        value = x.split('-')
        return value[0]
    return x  # Retourner la valeur originale si pas de '-' ou pas une chaîne

df['REFERENCE'] = df['REFERENCE'].apply(removeTrait)


df.to_excel(fileName)
"""
"""
fileName = "u-power.xlsx"
path = os.path.join(fileName)

brand ="UPOWER"

df = pd.read_excel(fileName)
df['brand'] = brand

df.to_excel(fileName)

"""


#add price
left  = "BOSCH.xlsx"
right = "BOSCH.xlsx"


# Lecture des fichiers Excel
left_df = pd.read_excel(os.path.join(left))  # Création d'un DataFrame à partir du fichier Excel gauche
right_df = pd.read_excel(os.path.join('../price', right))  # Création d'un DataFrame à partir du fichier Excel droit

# Fusion des DataFrames
merge = pd.merge(
    left=left_df,
    right=right_df[['REFERENCE', 'EAN', 'PRIX TARIF N']],
    how='left',  # 'left' était utilisé comme variable, remplacé par la string 'left'
    on='REFERENCE'
)


merge.to_excel(left)

"""

left = "u-power.xlsx"
left_df = pd.read_excel(os.path.join(left))

# Réindexer pour commencer à 10122
start_index = 10122
left_df.index = range(start_index, start_index + len(left_df))

left_df.to_excel(left)
"""
