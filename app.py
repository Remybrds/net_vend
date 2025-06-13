import streamlit as st
import pandas as pd

# Lecture des données
lien = "tableau_coeff.xlsx"
df = pd.read_excel(lien)

# Fonction de calcul
def prix_nv(prix_net_vendeur):
    if prix_net_vendeur : 
        prix_net_vendeur = int(prix_net_vendeur)
        for i in range(0, len(df)):
            if prix_net_vendeur >= df['min'][i] and prix_net_vendeur <= df['max'][i]:
                coeff_temp = df['coeff'][i]
                prix_vente_temp = prix_net_vendeur + (prix_net_vendeur * df['coeff'][i])
                if prix_net_vendeur + (prix_net_vendeur * df['coeff'][i]) > df['min'][i+1]:
                    prix_vente = prix_net_vendeur + (prix_net_vendeur * df['coeff'][i+1])
                    coeff = df['coeff'][i+1]
                    return coeff, prix_vente
                else:
                    return coeff_temp, prix_vente_temp
    else : exit

# --- STYLE MINIMALISTE ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        .big-number {
            font-size: 2em;
            font-weight: 600;
        }
        .label {
            font-size: 0.9em;
            color: #888;
            margin-top: -10px;
        }
        .box {
            border: 1px solid #eee;
            border-radius: 10px;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- UI ---
st.title("Calcul du prix de vente selon le prix de vente net client")

prix_net_vendeur = st.text_input("Entrez le prix net vendeur (€)", value=0, placeholder="Ex: 300000")
prix_net_vendeur = int(prix_net_vendeur.replace(" ", ""))

if prix_net_vendeur:
    try:
        prix_net_vendeur = int(prix_net_vendeur)
        coeff, prix_vente = prix_nv(prix_net_vendeur)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="box"><div class="big-number">{:.0f} €</div><div class="label">Prix net vendeur</div></div>'.format(prix_net_vendeur), unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="box"><div class="big-number">{:.3f}</div><div class="label">Coefficient appliqué</div></div>'.format(coeff), unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="box"><div class="big-number">{:.0f} €</div><div class="label">Prix de vente estimé</div></div>'.format(prix_vente), unsafe_allow_html=True)

        st.markdown("### Détails des coefficients utilisés")
        st.dataframe(df[['Prix_de_vente', 'coeff']])
    except:
        st.warning("Erreur : Veuillez entrer un nombre valide.")
else:
    st.info("Veuillez saisir un prix net vendeur pour lancer le calcul.")
