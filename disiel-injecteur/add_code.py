import pandas as pd
import re

# Fonction pour normaliser les références (en majuscules et sans "- _ ,")
def normalize_reference(ref):
    if pd.isna(ref) or not isinstance(ref, str) or ref.strip() == "":
        return None  # Retourne None si la référence est vide ou invalide
    return re.sub(r'[-_,]', '', ref).upper()  # Supprime les caractères et met en majuscules

# Charger les fichiers Excel
df1 = pd.read_excel("original.xlsx")  # Contient produit_id et référence du produit
df2 = pd.read_excel("clean_produits.xlsx")  # Contient référence du produit, code moteur et lien

# Ajouter une colonne "code_moteur" et "link" vide dans df1
df1["code_moteur"] = None
df1["link"] = None

# Appliquer la normalisation des références pour comparaison
df1["reference_clean"] = df1["reference"].astype(str).apply(normalize_reference)
df2["reference_clean"] = df2["reference"].astype(str).apply(normalize_reference)

# Créer un dictionnaire des références et codes moteurs + liens
reference_to_code_moteur = df2.set_index("reference_clean")["code_moteur"].to_dict()
reference_to_link = df2.set_index("reference_clean")["link"].to_dict()

# Fonction pour récupérer le code moteur avec gestion du "0" au début
def get_code_moteur(ref):
    if ref in reference_to_code_moteur:
        return reference_to_code_moteur[ref]  # Correspondance directe
    if ref and ref.startswith("0"):
        return reference_to_code_moteur.get(ref[1:], None)  # Test en enlevant "0"
    return reference_to_code_moteur.get("0" + ref, None)  # Test en ajoutant "0"

# Fonction pour récupérer le lien avec la même logique
def get_link(ref):
    if ref in reference_to_link:
        return reference_to_link[ref]  # Correspondance directe
    if ref and ref.startswith("0"):
        return reference_to_link.get(ref[1:], None)  # Test en enlevant "0"
    return reference_to_link.get("0" + ref, None)  # Test en ajoutant "0"

# Mettre à jour les colonnes "code_moteur" et "link" dans df1
df1["code_moteur"] = df1["reference_clean"].apply(get_code_moteur)
df1["link"] = df1["reference_clean"].apply(get_link)

# Supprimer la colonne temporaire
df1.drop(columns=["reference_clean"], inplace=True)

# Sauvegarder le fichier mis à jour
df1.to_excel("original_mis_a_jour.xlsx", index=False)

print("✅ Mise à jour terminée avec succès ! 🎉")
