import pandas as pd

# Charger le fichier Excel
fichier_excel = "cleaner.xlsx"  # Remplace par le nom de ton fichier
df = pd.read_excel(fichier_excel)

# Supprimer les lignes où 'code_moteur' est vide
df_cleaned = df.dropna(subset=['code_moteur'])

# Sauvegarder le fichier nettoyé
df_cleaned.to_excel("cleaner_clean.xlsx", index=False)

print("Les lignes avec 'code_moteur' vide ont été supprimées.")
