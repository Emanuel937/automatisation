import pandas as pd
import re

# Charger le fichier Excel
file_path = "injecteurs.xlsx"  # Remplace par ton fichier réel
df = pd.read_excel(file_path)

# Vérifier si la colonne 'title' existe
if 'title' in df.columns:

    def extract_reference(title):
        if pd.isna(title):
            return ""  # Gérer les valeurs NaN
        
        # Supprime les espaces en début et fin
        title = title.strip()
        
        # Supprimer le mot "neuf" à la fin s'il est présent
        title = re.sub(r"\bneuf\b", "", title, flags=re.IGNORECASE).strip()

        # Expression régulière pour capturer la référence à la fin
        pattern = re.compile(r"([A-Za-z0-9-]+)$")
        match = pattern.search(title)

        return match.group(1) if match else ""

    # Appliquer la fonction et créer la colonne 'reference'
    df['reference'] = df['title'].apply(extract_reference)

    # Sauvegarder le fichier mis à jour
    output_path = "injecteur_r.xlsx"
    df.to_excel(output_path, index=False)
    print(f"Fichier mis à jour et sauvegardé sous : {output_path}")

else:
    print("La colonne 'title' n'existe pas dans le fichier.")
