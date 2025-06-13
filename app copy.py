import streamlit as st
import pandas as pd

lien ="tableau_coeff.xlsx"
df = pd.read_excel(lien)

def prix_nv(prix_net_vendeur):
    if prix_net_vendeur :
        prix_net_vendeur = int(prix_net_vendeur.replace(" ", "")) if prix_net_vendeur else None
        for i in range(0, len(df)):
            #print(prix_net_vendeur)
            #print(df['Prix_de_vente'][i])
            if prix_net_vendeur >= df['min'][i] and prix_net_vendeur <= df['max'][i]:
                coeff_temp = df['coeff'][i]
                prix_vente_temp = prix_net_vendeur + (prix_net_vendeur * df['coeff'][i])
                #print(f'Coeff temporaire : ' ,coeff_temp)
                #print(f'prix_vente temporaire : ',prix_vente_temp)
                if prix_net_vendeur + (prix_net_vendeur * df['coeff'][i]) > df['min'][i+1] : 
                    prix_vente = prix_net_vendeur + (prix_net_vendeur * df['coeff'][i+1])
                    coeff = df['coeff'][i+1]
                    return coeff, prix_vente
                    #print(prix_vente, df['coeff'][i+1])
                    #print(prix_net_vendeur)
                    #print(f'Coeff : ' ,df['coeff'][i+1])
                    #print(f'prix_vente : ',prix_vente)
                else :
                    return coeff_temp, prix_vente_temp
                    #print(prix_net_vendeur)
                    #print(f'Coeff temporaire : ' ,coeff_temp)
                    #print(f'prix_vente temporaire : ',prix_vente_temp)

    else : exit

st.title("Calcul du prix de vente selon le prix de vente net client")

prix_net_vendeur = st.text_input("Inserez le prix net vendeur", "0")


if prix_net_vendeur:
    st.write("coeff appliqué : ",prix_nv(prix_net_vendeur)[0])
    st.write("coeff appliqué : ",prix_nv(prix_net_vendeur)[1])
    st.dataframe(df[['Prix_de_vente', 'coeff']])
else :
    st.write("")

