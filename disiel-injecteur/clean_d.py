import pandas as pd

# Charger le fichier Excel
df = pd.read_excel('other_cm.xlsx')

# Vérifier si la colonne "produit ID" existe
if 'Product ID' not in df.columns:
    print("❌ La colonne 'product ID' n'existe pas dans le fichier.")
else:
    # Supprimer les doublons en gardant la première occurrence
    df_cleaned = df.drop_duplicates(subset=['Product ID'], keep='first')

    # Sauvegarder le fichier nettoyé
    df_cleaned.to_excel('cleaner.xlsx', index=False)
    
    print(f"✅ Doublons supprimés ! Fichier mis à jour : {len(df) - len(df_cleaned)} lignes supprimées.")

