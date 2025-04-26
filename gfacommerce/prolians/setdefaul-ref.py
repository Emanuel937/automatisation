import pandas as pd

# Exemple de dictionnaires pour les parents et les enfants
parent_path = {
    'id': [1, 2, 3],
    'name': ['produit_1', 'produit_2', 'produit3']
}

children_path = {
    'parentId': [2, 2, 1],
    'reference': ['0N4', 'ZE10', '0P54']
}

# Création des DataFrames
parents  = pd.DataFrame(parent_path)
children = pd.DataFrame(children_path)

# Fusion des DataFrames sur la clé 'id' pour les parents et 'parentId' pour les enfants
merged = parents.merge(children[['reference', 'parentId']], left_on='id', right_on='parentId', how='left')

# Affichage du résultat
print(merged)
