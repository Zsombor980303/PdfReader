import streamlit as st
from pypdf import PdfReader
import json
from google import genai

client = genai.Client(api_key="EZ_EGY_KAMU_KULCS_A_GITHUB_MIATT_12345")

Pdf_to_analyze = PdfReader(uploaded_file)
AI_KAPCSOLO = True

teszt_adatok = [
    {
        'talalat_szovege': "A termék kiszállítása a rendeléstől számított 3-5 munkanapon belül megtörténik.",
        'ai_valasz': "A beküldött dokumentum alapján a szállítási határidő fixen 3-5 munkanap. Pénzügyi vonzata nincs.",
        'biztonsagi_kockazat': "Alacsony"
    },
    {
        'talalat_szovege': "A felhasználó jogosult a szolgáltatás azonnali felfüggesztésére, amennyiben technikai hiba lép fel.",
        'ai_valasz': "FIGYELEM! A rendszer súlyos belépési és technikai hibát észlelt, ami miatt a szolgáltatás leállt.",
        'biztonsagi_kockazat': "Magas"
    },
    {
        'talalat_szovege': "Jelen szerződés határozatlan időre köttetik, 30 napos felmondási idővel.",
        'ai_valasz': "A felhasználó kezdeményezte az előfizetés megszüntetését költözésre hivatkozva.",
        'biztonsagi_kockazat': "Közepes"
    }
]

if AI_KAPCSOLO == False:
    with open("ai_riport.json", "w", encoding="utf-8") as f:
        json.dump(teszt_adatok, f, ensure_ascii=False, indent=4)
    print("💾 Szuper! A kamu eredményeket elmentettem a 'ai_riport.json' fájlba.")
else:
    print('AI Version starting...')

    pdf_szoveg = ""
    for lap in Pdf_to_analyze.pages:
        szoveg = lap.extract_text()
        if szoveg:
            pdf_szoveg += szoveg + "\n"

    prompt = f"""
    Elemezd az alábbi dokumentum szövegét, és keress benne 3 olyan pontot, állítást vagy záradékot, ami jogi, pénzügyi vagy működési biztonsági kockázatot jelenthet!

    A választ kötelezően egyetlen tiszta JSON tömbként (listaként) kell visszaadnod, amely pontosan 3 darab JSON objektumot tartalmaz. Minden objektumnak szigorúan az alábbi 3 kulccsal kell rendelkeznie:
    - 'talalat_szovege': A dokumentumból kimásolt pontos mondat vagy bekezdés.
    - 'ai_valasz': Rövid elemzés, magyarázat és javaslat a kockázat kezelésére.
    - 'biztonsagi_kockazat': Kizárólag ezen három érték egyike lehet: 'Alacsony', 'Közepes' vagy 'Magas'.

    Dokumentum szövege:
    {pdf_szoveg}
    """

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt,
            response_format={"type": "text", "mime_type": "application/json"}
        )

        valodi_adatok = json.loads(interaction.output_text)
        with open("ai_riport.json", "w", encoding="utf-8") as f:
            json.dump(valodi_adatok, f, ensure_ascii=False, indent=4)
        print("💾 Szuper! A valódi AI eredményeket elmentettem.")

    except Exception as e:
        st.warning(
            "⚠️ A Google AI szervere jelenleg túlterhelt (503-as hiba). Kérlek, várj pár másodpercet, majd nyomd meg újra a gombot!")
        print(f"Szerver hiba részletei: {e}")