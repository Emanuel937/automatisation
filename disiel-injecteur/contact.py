import pandas as pd

# Charger les deux fichiers Excel
df1 = pd.read_excel("site.xlsx")
df2 = pd.read_excel("cleaner_clean.xlsx")

# Concaténer les fichiers (ajout de lignes)
df_final = pd.concat([df1, df2], ignore_index=True)

# Sauvegarder dans un nouveau fichier
df_final.to_excel("produits_avec_code_moteur.xlsx", index=False)

print("Fusion terminée avec succès ! 🎉")
