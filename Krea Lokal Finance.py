import streamlit as st
import pandas as pd
import os

# --- 1. PROTECTION PAR MOT DE PASSE ---
def check_password():
    """Fonction pour vérifier le mot de passe"""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.title("🔒 Accès sécurisé")
        password = st.text_input("Entrez votre mot de passe", type="password")
        if st.button("Valider"):
            if password == "860506": 
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect")
        return False
    return True

if not check_password():
    st.stop()

# --- 2. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Krea Lokal Finance", page_icon="💰", layout="wide")
st.title("💸 Krea Lokal Finance - Tableau de Bord")

FICHIER = "historique_krea.txt"

# --- 3. LISTES ET MENUS ---
liste_mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
liste_entrees = ["Bagatelle", "Wapalapam", "Attitude", "Cap Tamarin", "GBLC", "Market", "Direct Sales"]
liste_sorties = ["Account fees", "Shop rental", "MRA Payment", "Salaires", "Let's C", "ClickNBuy", "Carpouron", "Gazella", "Temu", "Print Card", "MIPS", "Shopify", "Visa License", "Accountant payment", "Other"]

# --- 4. ZONE DE SAISIE ---
st.subheader("📝 Ajouter une opération")
mois = st.selectbox("Sélectionnez le mois", liste_mois)
col_gauche, col_droite = st.columns(2)

with col_gauche:
    st.markdown("### 🟢 Entrées d'argent")
    cat_entree = st.selectbox("Catégorie", liste_entrees, key="cat_entree")
    montant_entree = st.number_input("Montant (MUR)", min_value=0.0, step=50.0, key="montant_entree")
    if st.button("💾 Enregistrer l'entrée"):
        with open(FICHIER, "a") as f:
            f.write(f"{mois} | Entrée | {cat_entree} | {montant_entree} MUR\n")
        st.success("✅ Entrée ajoutée !")
        st.rerun()

with col_droite:
    st.markdown("### 🔴 Sorties d'argent")
    cat_sortie = st.selectbox("Catégorie", liste_sorties, key="cat_sortie")
    montant_sortie = st.number_input("Montant (MUR)", min_value=0.0, step=50.0, key="montant_sortie")
    if st.button("💾 Enregistrer la sortie"):
        with open(FICHIER, "a") as f:
            f.write(f"{mois} | Sortie | {cat_sortie} | {-montant_sortie} MUR\n")
        st.success("✅ Sortie ajoutée !")
        st.rerun()

st.divider()

# --- 5. SUPPRESSION D'ERREUR ---
st.subheader("🗑️ Supprimer une erreur")
if os.path.exists(FICHIER):
    with open(FICHIER, "r") as f:
        lignes = f.readlines()
    if lignes:
        op_a_suppr = st.selectbox("Choisir l'opération à effacer :", lignes)
        if st.button("🚨 Supprimer définitivement"):
            lignes_restantes = [l for l in lignes if l != op_a_suppr]
            with open(FICHIER, "w") as f:
                f.writelines(lignes_restantes)
            st.success("✅ Opération supprimée !")
            st.rerun()

st.divider()

# --- 6. ANALYSE ET GRAPHIQUES ---
st.subheader("📊 Analyse de mes Finances")
if os.path.exists(FICHIER):
    with open(FICHIER, "r") as f:
        lignes = f.readlines()
    donnees = []
    for ligne in lignes:
        if "|" in ligne:
            el = ligne.split("|")
            donnees.append({"Mois": el[0].strip(), "Type": el[1].strip(), "Catégorie": el[2].strip(), "Montant": float(el[3].replace("MUR", "").strip())})
    
    if donnees:
        df = pd.DataFrame(donnees)
        c1, c2, c3 = st.columns(3)
        c1.metric("🟢 Total Entrées", f"{df[df['Type']=='Entrée']['Montant'].sum()} MUR")
        c2.metric("🔴 Total Sorties", f"{df[df['Type']=='Sortie']['Montant'].sum()} MUR")
        c3.metric("💰 SOLDE FINAL", f"{df['Montant'].sum()} MUR")
        
        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("**📉 Dépenses par Catégorie**")
            sorties = df[df["Type"]=="Sortie"].copy()
            if not sorties.empty:
                sorties["Dépense"] = sorties["Montant"].abs()
                st.bar_chart(sorties.groupby("Catégorie")["Dépense"].sum())
        with g2:
            st.markdown("**📈 Évolution du Profit par Mois**")
            st.line_chart(df.groupby("Mois")["Montant"].sum())
        
        st.markdown("**📔 Historique Complet**")
        st.dataframe(df, use_container_width=True)
else:
    st.info("Aucune donnée pour le moment.")
