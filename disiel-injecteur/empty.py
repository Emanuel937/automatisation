import pandas as pd

# Charger le fichier Excel
fichier_excel = "original_mis_a_jour.xlsx"  # Remplace par le nom de ton fichier
df = pd.read_excel(fichier_excel)

# Filtrer les lignes où 'code_moteur' est vide
df_vide = df[df['code_moteur'].isna()]

# Sauvegarder le résultat dans un nouveau fichier
df_vide.to_excel("site_code_moteur_vide.xlsx", index=False)

print("Les lignes avec 'code_moteur' vide ont été récupérées et enregistrées.")
