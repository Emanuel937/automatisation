import pandas as pd

# Charger le fichier Excel
file_path = "cleaner.xlsx"  # Remplace par le bon chemin
df = pd.read_excel(file_path)

# Vérifier si la colonne 'code_moteur' existe
if 'code_moteur' in df.columns:
    # Filtrer uniquement les lignes où 'code_moteur' est vide ou NaN
    df_filtre = df[df['code_moteur'].isna() | (df['code_moteur'] == '')]

    # Sauvegarder dans un nouveau fichier Excel
    output_path = "produits_sans_code.xlsx"
    df_filtre.to_excel(output_path, index=False)
    print(f"Fichier filtré sauvegardé sous : {output_path}")
else:
    print("La colonne 'code_moteur' n'existe pas dans le fichier.")
