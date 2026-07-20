import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
import piexif
from io import BytesIO

st.set_page_config(page_title="Formulaire EXIF", layout="centered")

st.title("Éditeur de métadonnées EXIF", text_alignment="center")

uploaded_image = st.file_uploader("Importer une image", type=["jpg", "jpeg"])

if uploaded_image:
    image_bytes = uploaded_image.getvalue()
    image = Image.open(BytesIO(image_bytes))
    exif_bytes = image.info.get("exif")

    if exif_bytes:
        exif_dict = piexif.load(exif_bytes)
    else:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    st.image(image, caption="Image originale", use_container_width=True)

    st.subheader("Modifier les métadonnées EXIF")
    
    auteur = st.text_input("Auteur")
    copyright = st.text_input("Copyright")
    description = st.text_area("Description de l'image")
    marque = st.text_input("Marque")
    modele = st.text_input("Modèle")
    logiciel = st.text_input("Logiciel utilisé")
    date_time = st.text_input("Date de prise (YYYY:MM:DD HH:MM:SS)")

    if auteur:
        exif_dict["0th"][piexif.ImageIFD.Artist] = auteur.encode()
    if copyright:
        exif_dict["0th"][piexif.ImageIFD.Copyright] = copyright.encode()
    if description:
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode()
    if marque:
        exif_dict["0th"][piexif.ImageIFD.Make] = marque.encode()
    if modele:
        exif_dict["0th"][piexif.ImageIFD.Model] = modele.encode()
    if logiciel:
        exif_dict["0th"][piexif.ImageIFD.Software] = logiciel.encode()
    if date_time:
        exif_dict["0th"][piexif.ImageIFD.DateTime] = date_time.encode()

    st.subheader("Coordonnées GPS à insérer")

    latitude = st.number_input("Latitude", value=45.01)
    longitude = st.number_input("Longitude", value=5.56)

    latitude_str = f"{latitude}"
    longitude_str = f"{longitude}"

    exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = latitude_str.encode()
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = latitude_str.encode()

    carte = folium.Map(location=[latitude, longitude], zoom_start=7)

    folium.Marker([latitude, longitude], tooltip="Emplacement GPS").add_to(carte)

    st.subheader("Carte de localisation (selon les coordonnées GPS saisies)")
    
    st_folium(carte, width=700, height=500)

    if st.button("Enregistrer les métadonnées EXIF"):
        exif_bytes_new = piexif.dump(exif_dict)
        sortie = BytesIO()
        image.save(sortie, format="JPEG", exif=exif_bytes_new)
        st.session_state["image_modifiee"] = sortie.getvalue()
        st.success("Métadonnées EXIF mises à jour avec succès !")

    if "image_modifiee" in st.session_state:
        st.download_button(label="Télécharger l'image modifiée", data=st.session_state["image_modifiee"], file_name="image_modifiee.jpg", mime="image/jpeg")


st.subheader("Carte avec les coordonnées de mes destinations de rêve")

coords = [
    ("Celje", 46.25, 15.25), 
    ("Rome", 41.95, 12.50),
    ("Paris", 48.82, 2.34),
    ("Londres", 51.15, -0.18),
    ("Lisbonne", 38.72, -9.15)
]

points = []

maps = folium.Map(location=[48.82, 2.34], zoom_start=4)

for ville, lat, long in coords:
    folium.Marker([lat, long], tooltip=ville).add_to(maps)
    points.append([lat, long])

folium.PolyLine(points, weight=3).add_to(maps)

st_folium(maps, width=725, height=500)