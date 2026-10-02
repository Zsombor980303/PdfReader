
import streamlit as st
import pandas as pd
from pypdf import PdfReader
import json
from google import genai

client = genai.Client(api_key="EZ_EGY_KAMU_KULCS_A_GITHUB_MIATT_12345")

#from web_page import uploaded_file #nem kell ez ide, mert a web_page-ben exec(f.read)-et használjuk, ami miatt már eléri a változókat. Ha ezt ideírom, akkor duplikáció miatt hibát dob

Pdf_to_analyze = PdfReader(uploaded_file) #nem valós hiba
print(f'Pdf: {Pdf_to_analyze}')
AI_KAPCSOLO = True

# Teszt adatok betöltése, már eleve json formátumban
teszt_adatok = {
    'talalat_szovege': [
        "A termék kiszállítása a rendeléstől számított 3-5 munkanapon belül megtörténik.",
        "A felhasználó jogosult a szolgáltatás azonnali felfüggesztésére, amennyiben technikai hiba lép fel.",
        "Jelen szerződés határozatlan időre köttetik, 30 napos felmondási idővel."
    ],
    'ai_valasz': [
        "A beküldött dokumentum alapján a szállítási határidő fixen 3-5 munkanap. Pénzügyi vonzata nincs.",
        "FIGYELEM! A rendszer súlyos belépési és technikai hibát észlelt, ami miatt a szolgáltatás leállt.",
        "A felhasználó kezdeményezte az előfizetés megszüntetését költözésre hivatkozva."
    ],
    'biztonsagi_kockazat': ['Alacsony', 'Magas', 'Közepes']
}

if AI_KAPCSOLO == False:
    df = pd.DataFrame(teszt_adatok)
    print(df[['talalat_szovege', 'ai_valasz', 'biztonsagi_kockazat']])
    # Excel file-ba mentés
    df.to_excel("pdf_excel.xlsx", index=False)
    print("💾 Szuper! Az eredményeket elmentettem a 'pdf_excel.xlsx' fájlba.")
else:
    print('AI Version starting...')
    pdf_szoveg = ""
    for lap in Pdf_to_analyze.pages:
        szoveg = lap.extract_text()
        if szoveg:
            pdf_szoveg += szoveg + "\n"

    # 2. Elküldjük a tegnapi bevált input formátumban egybefüggő szövegként
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=f"""
        Foglald össze nekem maximum 3 mondatban, hogy miről szól az alábbi dokumentum!

        Dokumentum szövege:
        {pdf_szoveg}
        """
    )
    #data = json.loads(interaction.output_text)
    #df = pd.DataFrame(data)
    st.write(interaction.output_text)





