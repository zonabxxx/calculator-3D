import streamlit as st
import pandas as pd
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

# Konfigurácia stránky
st.set_page_config(
    page_title="Kazetové 3D Písmená - Kalkulátor",
    page_icon="🔤",
    layout="wide"
)

# Načítanie dát z Excel súboru
@st.cache_data
def load_pricing_data():
    """Načítanie cenových dát z Excel súboru"""
    try:
        df = pd.read_excel('Svetelná reklama.xlsx')
        return df
    except:
        return None

# Hlavička
st.title("🔤 Kazetové 3D Písmená - Kalkulátor")
st.markdown("---")

# Načítanie dát
pricing_df = load_pricing_data()

if pricing_df is None:
    st.error("❌ Nepodarilo sa načítať cenové dáta z Excel súboru!")
    st.stop()

# Hlavný formulár
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Kalkulácia kazetových 3D písmen")
    
    # Základné údaje
    st.subheader("Základné údaje")
    nazov_projektu = st.text_input("Názov projektu")
    zakaznik = st.text_input("Zákazník")
    datum = st.date_input("Dátum", datetime.now())
    
    # Parametre písmen
    st.subheader("Parametre písmen")
    
    # Výška písmen
    vyska_pismen = st.selectbox(
        "Výška písmen",
        ["do 20cm", "do 30cm", "do 40cm", "do 50cm", "do 60cm", 
         "do 70cm", "do 80cm", "do 90cm", "do 100cm", "do 150cm"]
    )
    
    # Počet písmen
    pocet_pismen = st.number_input("Počet písmen", min_value=1, value=5, step=1)
    
    # Materiál
    material = st.selectbox(
        "Materiál",
        ["10mm PVC", "5mm PLEXI"]
    )
    
    # Osvetlenie
    osvetlenie = st.checkbox("LED osvetlenie")
    
    # Montáž
    montaz = st.checkbox("Montáž a inštalácia")
    
    # Dodatočné služby
    st.subheader("Dodatočné služby")
    col_dod1, col_dod2 = st.columns(2)
    with col_dod1:
        lakovanie = st.checkbox("Lakovanie")
        foliovanie = st.checkbox("Fóliovanie")
    with col_dod2:
        doprava = st.checkbox("Doprava")
        navrh = st.checkbox("Grafický návrh")
    
    # Poznámky
    poznamky = st.text_area("Poznámky")

with col2:
    st.header("Kalkulácia")
    
    # Mapovanie výšky na stĺpec v Excel (s medzerami na konci!)
    vyska_mapping = {
        "do 20cm": "KP / do 20cm ",
        "do 30cm": "KP / do 30cm ",
        "do 40cm": "KP / do 40cm ",
        "do 50cm": "KP / do 50cm ",
        "do 60cm": "KP / do 60cm ",
        "do 70cm": "KP / do 70cm ",
        "do 80cm": "KP / do 80cm ",
        "do 90cm": "KP / do 90cm ",
        "do 100cm": "KP / do 100cm ",
        "do 150cm": "KP / do 150cm "
    }
    
    stlpec_vysky = vyska_mapping[vyska_pismen]
    
    # Získanie cien z Excel tabuľky
    try:
        # Riadok 15 obsahuje celkové náklady (Náklad)
        naklady_na_pismeno = pricing_df.loc[15, stlpec_vysky]
        
        # Riadok 17 obsahuje predajnú cenu (Predaj)
        predajna_cena_na_pismeno = pricing_df.loc[17, stlpec_vysky]
        
        # Základná cena za všetky písmená
        zakladna_cena = predajna_cena_na_pismeno * pocet_pismen
        
        st.metric("Počet písmen", pocet_pismen)
        st.metric("Výška písmen", vyska_pismen)
        st.metric("Cena za 1 písmeno", f"{predajna_cena_na_pismeno:.2f} €")
        
        # Prirážky
        prirazky = 0
        
        if lakovanie:
            prirazka_lakovanie = zakladna_cena * 0.15  # 15% za lakovanie
            prirazky += prirazka_lakovanie
            st.write(f"Lakovanie (15%): {prirazka_lakovanie:.2f} €")
        
        if foliovanie:
            prirazka_foliovanie = zakladna_cena * 0.20  # 20% za fóliovanie
            prirazky += prirazka_foliovanie
            st.write(f"Fóliovanie (20%): {prirazka_foliovanie:.2f} €")
        
        if osvetlenie:
            # LED moduly a zdroj z Excel tabuľky
            led_modul_cena = pricing_df.loc[4, stlpec_vysky] * pocet_pismen  # Led modul
            led_zdroj_cena = pricing_df.loc[5, stlpec_vysky] * pocet_pismen   # LED zdroj
            osvetlenie_cena = led_modul_cena + led_zdroj_cena
            prirazky += osvetlenie_cena
            st.write(f"LED osvetlenie: {osvetlenie_cena:.2f} €")
        
        if montaz:
            montaz_cena = zakladna_cena * 0.25  # 25% za montáž
            prirazky += montaz_cena
            st.write(f"Montáž (25%): {montaz_cena:.2f} €")
        
        if doprava:
            doprava_cena = 50  # Fixná cena za dopravu
            prirazky += doprava_cena
            st.write(f"Doprava: {doprava_cena:.2f} €")
        
        if navrh:
            navrh_cena = 100  # Fixná cena za návrh
            prirazky += navrh_cena
            st.write(f"Grafický návrh: {navrh_cena:.2f} €")
        
        # Celková cena
        celkova_cena = zakladna_cena + prirazky
        
        st.markdown("---")
        st.subheader("Rozpis cien")
        st.write(f"Základná cena ({pocet_pismen}x {predajna_cena_na_pismeno:.2f}€): {zakladna_cena:.2f} €")
        if prirazky > 0:
            st.write(f"Prirážky celkom: {prirazky:.2f} €")
        
        st.markdown("---")
        st.metric("**CELKOVÁ CENA**", f"{celkova_cena:.2f} €")
        
        # Marža z Excel súboru
        marza_excel = pricing_df.loc[19, stlpec_vysky] * 100  # Riadok 19 = marža v desatinnom tvare
        st.metric("Marža (z Excel)", f"{marza_excel:.1f}%")
        
    except Exception as e:
        st.error(f"Chyba pri výpočte: {e}")
        st.write(f"Debug info: {e}")
        celkova_cena = 0
        zakladna_cena = 0

# Tlačidlo na generovanie PDF
if st.button("📄 Generovať PDF ponuku", type="primary"):
    if nazov_projektu and zakaznik:
        # Vytvorenie PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Vytvorenie vlastného štýlu s podporou UTF-8
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.fonts import addMapping
        
        # Registrácia fontu s podporou diakritiky
        try:
            # Pokus o použitie DejaVu Sans fontu (má dobrú podporu pre slovenčinu)
            import os
            font_paths = [
                '/System/Library/Fonts/Arial.ttf',  # macOS
                '/System/Library/Fonts/Helvetica.ttc',  # macOS
                'C:\\Windows\\Fonts\\arial.ttf',  # Windows
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
            ]
            
            font_registered = False
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('CustomFont', font_path))
                        font_name = 'CustomFont'
                        font_registered = True
                        break
                    except:
                        continue
            
            if not font_registered:
                font_name = 'Helvetica'
        except:
            font_name = 'Helvetica'
        
        story = []
        
        # Nadpis
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Center
            fontName=font_name
        )
        story.append(Paragraph("PONUKA - KAZETOVÉ 3D PÍSMENÁ", title_style))
        story.append(Spacer(1, 20))
        
        # Základné údaje
        data = [
            ['Projekt:', nazov_projektu],
            ['Zákazník:', zakaznik],
            ['Dátum:', datum.strftime('%d.%m.%Y')],
            ['Počet písmen:', str(pocet_pismen)],
            ['Výška písmen:', vyska_pismen],
            ['Materiál:', material]
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), font_name),
            ('FONTNAME', (1, 0), (1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Cenová kalkulácia
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontName=font_name
        )
        story.append(Paragraph("CENOVÁ KALKULÁCIA", heading_style))
        
        cena_data = [['Položka', 'Cena (€)']]
        cena_data.append(['Základná cena', f'{zakladna_cena:.2f}'])
        
        if lakovanie:
            cena_data.append(['Lakovanie', f'{zakladna_cena * 0.15:.2f}'])
        if foliovanie:
            cena_data.append(['Fóliovanie', f'{zakladna_cena * 0.20:.2f}'])
        if osvetlenie:
            cena_data.append(['LED osvetlenie', f'{osvetlenie_cena:.2f}'])
        if montaz:
            cena_data.append(['Montáž', f'{zakladna_cena * 0.25:.2f}'])
        if doprava:
            cena_data.append(['Doprava', '50.00'])
        if navrh:
            cena_data.append(['Grafický návrh', '100.00'])
        
        cena_data.append(['CELKOM', f'{celkova_cena:.2f}'])
        
        cena_table = Table(cena_data, colWidths=[3*inch, 2*inch])
        cena_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(cena_table)
        
        if poznamky:
            story.append(Spacer(1, 20))
            notes_style = ParagraphStyle(
                'CustomNotes',
                parent=styles['Heading2'],
                fontName=font_name
            )
            story.append(Paragraph("POZNÁMKY", notes_style))
            
            notes_content_style = ParagraphStyle(
                'CustomNotesContent',
                parent=styles['Normal'],
                fontName=font_name
            )
            story.append(Paragraph(poznamky, notes_content_style))
        
        doc.build(story)
        buffer.seek(0)
        
        # Download tlačidlo
        st.download_button(
            label="⬇️ Stiahnuť PDF",
            data=buffer,
            file_name=f"ponuka_3d_pismena_{nazov_projektu.replace(' ', '_')}_{datum.strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        
        st.success("PDF ponuka bola vygenerovaná!")
    else:
        st.error("Vyplňte prosím názov projektu a zákazníka!")

# Zobrazenie cenníka
with st.expander("📊 Cenník kazetových 3D písmen"):
    if pricing_df is not None:
        st.subheader("Predajné ceny za 1 písmeno (€)")
        
        # Vytvorenie tabuľky s cenami
        vysky = ["do 20cm", "do 30cm", "do 40cm", "do 50cm", "do 60cm", 
                "do 70cm", "do 80cm", "do 90cm", "do 100cm", "do 150cm"]
        
        cennik_data = []
        for vyska in vysky:
            stlpec = f"KP / {vyska} "  # S medzerou na konci!
            try:
                cena = pricing_df.loc[17, stlpec]  # Riadok 17 = predajná cena
                cennik_data.append([vyska, f"{cena:.2f} €"])
            except:
                cennik_data.append([vyska, "N/A"])
        
        cennik_df = pd.DataFrame(cennik_data, columns=["Výška písmena", "Cena za kus"])
        st.table(cennik_df)
        
        # Zobrazenie marže
        st.subheader("Marža podľa výšky písmen")
        marza_data = []
        for vyska in vysky:
            stlpec = f"KP / {vyska} "  # S medzerou na konci!
            try:
                marza_decimal = pricing_df.loc[19, stlpec]  # Riadok 19 = marža v desatinnom tvare
                marza_percent = marza_decimal * 100  # Konverzia na percentá
                marza_data.append([vyska, f"{marza_percent:.0f}%"])
            except:
                marza_data.append([vyska, "N/A"])
        
        marza_df = pd.DataFrame(marza_data, columns=["Výška písmena", "Marža"])
        st.table(marza_df) 