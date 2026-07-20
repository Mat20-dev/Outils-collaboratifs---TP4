import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Bonus - Pi et dates", layout="centered")
st.title("Recherche dans les décimales de π")

def charger_pi():
    try:
        with open("1000000.txt", "r") as fp:
            return fp.read().strip()
    except FileNotFoundError:
        st.error("Le fichier 1000000.txt est introuvable.")

pi_million = charger_pi()

date_naissance = st.text_input("Entres ta date de naissance :", placeholder="Exemple : 15092005", max_chars=8)

if st.button("Rechercher"):
    if len(date_naissance) != 8 or not date_naissance.isdigit():
        st.warning("Merci de saisir une date de naissance au format JJMMAAAA.")
    else:
        if date_naissance in pi_million:
            position = pi_million.find(date_naissance)
            st.success(f"Ta date de naissance apparaît dans le premier million de décimales de PI à la position {position}.")
        else:
            st.warning("Ta date de naissance n'apparaît pas dans le premier million de décimales de PI.")
    try:
            date = datetime.strptime(date_naissance, "%d%m%Y")
            jour = date.strftime("%A")

            jours_fr = {
                "Monday": "Lundi",
                "Tuesday": "Mardi",
                "Wednesday": "Mercredi",
                "Thursday": "Jeudi",
                "Friday": "Vendredi",
                "Saturday": "Samedi",
                "Sunday": "Dimanche"
            }

            st.info(f"Tu es né(e) un {jours_fr[jour]}.")

    except ValueError:
         st.error("La date de naissance est invalide.")

st.subheader("Sommes des décimales de π")

somme20 = 0

for chiffre in pi_million[2:22]:
    somme20 = somme20 + int(chiffre)

somme144 = 0

for chiffre in pi_million[2:146]:
    somme144 = somme144 + int(chiffre)

st.text(f"Somme des 20 premières décimales de PI : {somme20}")
st.text(f"Somme des 144 premières décimales de PI : {somme144}")

if somme20 == somme144:
    st.success("Les deux sommes sont identiques.")
else:
    st.info("Les deux sommes sont différentes.")

st.subheader("La somme des nombres naturels et -1/12")

st.video("https://www.youtube.com/watch?v=GnZQOb9YNV4")