import streamlit as st
import os
import time

st.set_page_config(page_title="PDF AI Assistant", page_icon="📄")
st.title("📄 PDF AI Assistant")

uploaded_file = st.file_uploader(label='Choose a pdf file', type=["pdf"])

if uploaded_file is not None:
    st.success(f"Successfully uploaded a pdf file: {uploaded_file.name}")

    if st.button('Start AI Assistant'):
        with st.spinner('AI Assistant is working right now...'):
            with open("main.py", "r", encoding="utf-8") as f:
                exec(f.read())

            st.success("✅ Sikeres elemzés!")
            time.sleep(2)
            st.rerun()

    eredmeny_fajl = "ai_riport.json"

    if os.path.exists(eredmeny_fajl):
        import json

        with open(eredmeny_fajl, "r", encoding="utf-8") as f:
            adatok = json.load(f)

        st.subheader("🤖 Az AI elemzés részletes eredményei")

        # Végigmegyünk a talált kockázatokon (amiket a main.py mentett le)
        for i, elem in enumerate(adatok):
            kockazat = elem.get('biztonsagi_kockazat', 'Közepes')

            # Beépített színkódolás a szöveg elé
            szin = "🟢" if kockazat == "Alacsony" else "🟡" if kockazat == "Közepes" else "🔴"

            # Lenyitható dobozba tesszük a találatokat
            with st.expander(f"{szin} {i + 1}. Találat - Kockázati szint: {kockazat}"):
                st.markdown(f"**Kockázatos mondat a PDF-ből:**")
                st.info(elem.get('talalat_szovege', ''))

                st.markdown(f"**AI magyarázat és javaslat:**")
                st.write(elem.get('ai_valasz', ''))
    else:
        st.warning("⚠️ Nem található korábbi elemzés. Nyomd meg a gombot az indításhoz!")