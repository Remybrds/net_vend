import streamlit as st
import pandas as pd

# Lecture des données
lien = "tableau_coeff.xlsx"
df = pd.read_excel(lien)

# Fonction de calcul
def prix_nv_c(prix_net_vendeur):
    if prix_net_vendeur : 
        for i in range(3, len(df)):
            if prix_net_vendeur >= df['min'][i] and prix_net_vendeur <= df['max'][i]:
                coeff_temp = df['coeff'][i]
                prix_vente_temp = prix_net_vendeur / (1 - df['coeff'][i])
                if prix_net_vendeur / (1 - df['coeff'][i]) >= df['min'][i+1]:
                    prix_vente = prix_net_vendeur / ( 1 - df['coeff'][i+1])
                    coeff = df['coeff'][i+1]
                    return coeff, prix_vente
                else:
                    return coeff_temp, prix_vente_temp
    else : exit


def prix_nv_f(prix_net_vendeur): 
    if prix_net_vendeur : 
        for i in range(0, 2):
            if prix_net_vendeur >= df['min'][i] and prix_net_vendeur <= df['max'][i]:
                fixe_temp = df['coeff'][i]
                prix_vente_temp = prix_net_vendeur + fixe_temp
                if prix_net_vendeur + fixe_temp >= df['min'][i+1]:
                    prix_vente = prix_net_vendeur + df['coeff'][i+1]
                    coeff = df['coeff'][i+1]
                    return coeff, prix_vente
                else:
                    return fixe_temp, prix_vente_temp
        if prix_net_vendeur >= df['min'][2] and prix_net_vendeur <= df['max'][2]: 
            coeff_temp = df['coeff'][2]
            prix_vente_temp = prix_net_vendeur + coeff_temp
            if prix_net_vendeur + coeff_temp >= df['min'][3]:
                    prix_vente = prix_net_vendeur / (1 - df['coeff'][3])
                    coeff = df['coeff'][3]
                    return coeff, prix_vente
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
st.title("Estimation du prix de vente selon le prix net client")

prix_net_vendeur = st.text_input("Entrez le prix net vendeur (€)", placeholder="Ex: 300 000")
if prix_net_vendeur : 
    prix_net_vendeur = float(prix_net_vendeur.replace(" ", ""))

if prix_net_vendeur:
    try:
        prix_net_vendeur = float(prix_net_vendeur)
        if prix_net_vendeur > df['min'][0] and prix_net_vendeur <= df['max'][2]: 
            coeff, prix_vente = prix_nv_f(prix_net_vendeur)
        else : 
            coeff, prix_vente = prix_nv_c(prix_net_vendeur)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="box"><div class="big-number">{:.0f} €</div><div class="label">Prix net vendeur</div></div>'.format(prix_net_vendeur), unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="box"><div class="big-number">{:.3f}</div><div class="label">Coefficient appliqué</div></div>'.format(coeff), unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="box"><div class="big-number">{:.0f} €</div><div class="label">Prix de vente estimé</div></div>'.format(prix_vente), unsafe_allow_html=True)

        st.header("Barème")
        st.dataframe(df[['Prix_de_vente', 'coeff']].rename(columns={'Prix_de_vente' : 'Prix de vente', 'coeff' : 'Taux'}), )


        st.markdown("### Zone de vérif : ")
        prix_vente_final = st.text_input("Entrez le prix de vente total (€)", placeholder="Ex: 300 000")
        prix_vente_final = float(prix_vente_final)
        c=0
        p_net=0

        for i in range(0,3):
            if prix_vente_final >= df['min'][i] and prix_vente_final <= df['max'][i]:
                c = df['coeff'][i]
                p_net = prix_vente_final - c
                col4, col5, col6 = st.columns(3)
                with col4:
                    st.markdown('<div class="box"><div class="big-number">{:.0f} €</div><div class="label">Prix net vendeur</div></div>'.format(prix_vente_final), unsafe_allow_html=True)
                with col5:
                    st.markdown('<div class="box"><div class="big-number">{:.3f}</div><div class="label">Coefficient appliqué</div></div>'.format(c), unsafe_allow_html=True)
                with col6:
                    st.markdown('<div class="box"><div class="big-number">{:.0f} €</div><div class="label">Prix net vendeur</div></div>'.format(p_net), unsafe_allow_html=True)
                break

        for i in range(3, len(df)):
            if prix_vente_final >= df['min'][i] and prix_vente_final <= df['max'][i]:
                c = df['coeff'][i]
                p_net = prix_vente_final - (prix_vente_final * c)
                col4, col5, col6 = st.columns(3)
                with col4:
                    st.markdown('<div class="box"><div class="big-number">{:.0f} €</div><div class="label">Prix net vendeur</div></div>'.format(prix_vente_final), unsafe_allow_html=True)
                with col5:
                    st.markdown('<div class="box"><div class="big-number">{:.3f}</div><div class="label">Coefficient appliqué</div></div>'.format(c), unsafe_allow_html=True)
                with col6:
                    st.markdown('<div class="box"><div class="big-number">{:.0f} €</div><div class="label">Prix net vendeur</div></div>'.format(p_net), unsafe_allow_html=True)
                break
        
    except:
        st.info("Veuillez saisir un prix de vente total pour lancer le calcul")
else:
    st.info("Veuillez saisir un prix net vendeur pour lancer le calcul.")
