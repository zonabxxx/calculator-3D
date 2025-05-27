import streamlit as st
import pandas as pd
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# Konfigurácia stránky
st.set_page_config(
    page_title="Kalkulátor svetelných reklám",
    page_icon="💡",
    layout="wide"
)

# Hlavička
st.title("💡 Kalkulátor svetelných reklám")
st.markdown("---")

# Sidebar pre výber typu reklamy
st.sidebar.header("Typ svetelnej reklamy")
typ_reklamy = st.sidebar.selectbox(
    "Vyberte typ reklamy:",
    ["LED panel", "Neonová reklama", "Svetelný box"]
)

# Hlavný formulár
col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"Kalkulácia pre: {typ_reklamy}")
    
    # Základné údaje
    st.subheader("Základné údaje")
    nazov_projektu = st.text_input("Názov projektu")
    zakaznik = st.text_input("Zákazník")
    datum = st.date_input("Dátum", datetime.now())
    
    # Rozměry
    st.subheader("Rozmery")
    col_sirka, col_vyska = st.columns(2)
    with col_sirka:
        sirka = st.number_input("Šírka (cm)", min_value=0.0, value=100.0, step=1.0)
    with col_vyska:
        vyska = st.number_input("Výška (cm)", min_value=0.0, value=50.0, step=1.0)
    
    # Špecifické parametre podľa typu reklamy
    if typ_reklamy == "LED panel":
        st.subheader("LED panel - špecifikácie")
        rozlisenie = st.selectbox("Rozlíšenie", ["P2.5", "P3", "P4", "P5", "P6", "P8", "P10"])
        jas = st.number_input("Jas (nits)", min_value=1000, value=5000, step=500)
        vnutorne_vonkajsie = st.radio("Umiestnenie", ["Vnútorné", "Vonkajšie"])
        farby = st.selectbox("Farebnosť", ["Plnofarebný", "Jednofarebný", "Dvojfarebný"])
        
    elif typ_reklamy == "Neonová reklama":
        st.subheader("Neonová reklama - špecifikácie")
        typ_neonu = st.selectbox("Typ neónu", ["Klasický neón", "LED neón", "EL wire"])
        farba = st.selectbox("Farba", ["Červená", "Modrá", "Zelená", "Žltá", "Biela", "RGB"])
        hrubka = st.selectbox("Hrúbka (mm)", ["8", "10", "12", "15", "18"])
        tvar = st.selectbox("Tvar", ["Rovný", "Zakrivený", "Komplexný"])
        
    elif typ_reklamy == "Svetelný box":
        st.subheader("Svetelný box - špecifikácie")
        material = st.selectbox("Materiál", ["Akrylát", "Polykarbonát", "Plexisklo"])
        osvetlenie = st.selectbox("Osvetlenie", ["LED pásy", "Neónové trubice", "Halogénové"])
        hrubka_materialu = st.selectbox("Hrúbka materiálu (mm)", ["3", "5", "8", "10"])
        jednostranne_obojstranne = st.radio("Osvetlenie", ["Jednostranné", "Obojstranné"])
    
    # Dodatočné možnosti
    st.subheader("Dodatočné možnosti")
    col_dod1, col_dod2 = st.columns(2)
    with col_dod1:
        montaz = st.checkbox("Montáž")
        doprava = st.checkbox("Doprava")
        navrh = st.checkbox("Grafický návrh")
    with col_dod2:
        zaruka = st.selectbox("Záruka", ["1 rok", "2 roky", "3 roky", "5 rokov"])
        priorita = st.selectbox("Priorita", ["Štandardná", "Expresná"])
    
    # Poznámky
    poznamky = st.text_area("Poznámky")

with col2:
    st.header("Kalkulácia")
    
    # Výpočet plochy
    plocha_m2 = (sirka * vyska) / 10000  # cm² na m²
    st.metric("Plocha", f"{plocha_m2:.2f} m²")
    
    # Základné ceny podľa typu (ukážkové ceny)
    zakladne_ceny = {
        "LED panel": {
            "P2.5": 800, "P3": 600, "P4": 450, "P5": 350, "P6": 280, "P8": 200, "P10": 150
        },
        "Neonová reklama": {
            "Klasický neón": 120, "LED neón": 80, "EL wire": 40
        },
        "Svetelný box": {
            "LED pásy": 150, "Neónové trubice": 100, "Halogénové": 80
        }
    }
    
    # Výpočet základnej ceny
    if typ_reklamy == "LED panel":
        zakladna_cena_m2 = zakladne_ceny[typ_reklamy][rozlisenie]
        if vnutorne_vonkajsie == "Vonkajšie":
            zakladna_cena_m2 *= 1.3
        if farby == "Plnofarebný":
            zakladna_cena_m2 *= 1.5
        elif farby == "Dvojfarebný":
            zakladna_cena_m2 *= 1.2
            
    elif typ_reklamy == "Neonová reklama":
        zakladna_cena_m2 = zakladne_ceny[typ_reklamy][typ_neonu]
        if tvar == "Komplexný":
            zakladna_cena_m2 *= 1.8
        elif tvar == "Zakrivený":
            zakladna_cena_m2 *= 1.3
            
    elif typ_reklamy == "Svetelný box":
        zakladna_cena_m2 = zakladne_ceny[typ_reklamy][osvetlenie]
        if jednostranne_obojstranne == "Obojstranné":
            zakladna_cena_m2 *= 1.6
    
    zakladna_cena = plocha_m2 * zakladna_cena_m2
    
    # Prirážky
    cena_montaz = zakladna_cena * 0.15 if montaz else 0
    cena_doprava = 50 if doprava else 0
    cena_navrh = 100 if navrh else 0
    
    if priorita == "Expresná":
        prirazka_priorita = zakladna_cena * 0.25
    else:
        prirazka_priorita = 0
    
    # Celková cena
    celkova_cena = zakladna_cena + cena_montaz + cena_doprava + cena_navrh + prirazka_priorita
    
    # Zobrazenie cien
    st.subheader("Rozpis cien")
    st.write(f"Základná cena: {zakladna_cena:.2f} €")
    if montaz:
        st.write(f"Montáž (15%): {cena_montaz:.2f} €")
    if doprava:
        st.write(f"Doprava: {cena_doprava:.2f} €")
    if navrh:
        st.write(f"Grafický návrh: {cena_navrh:.2f} €")
    if priorita == "Expresná":
        st.write(f"Expresná priorita (25%): {prirazka_priorita:.2f} €")
    
    st.markdown("---")
    st.metric("**CELKOVÁ CENA**", f"{celkova_cena:.2f} €", delta=None)

# Tlačidlo na generovanie PDF
if st.button("📄 Generovať PDF ponuku", type="primary"):
    if nazov_projektu and zakaznik:
        # Vytvorenie PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Nadpis
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("PONUKA - SVETELNÁ REKLAMA", title_style))
        story.append(Spacer(1, 20))
        
        # Základné údaje
        data = [
            ['Projekt:', nazov_projektu],
            ['Zákazník:', zakaznik],
            ['Dátum:', datum.strftime('%d.%m.%Y')],
            ['Typ reklamy:', typ_reklamy],
            ['Rozmery:', f'{sirka} x {vyska} cm'],
            ['Plocha:', f'{plocha_m2:.2f} m²']
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Cenová kalkulácia
        story.append(Paragraph("CENOVÁ KALKULÁCIA", styles['Heading2']))
        
        cena_data = [['Položka', 'Cena (€)']]
        cena_data.append(['Základná cena', f'{zakladna_cena:.2f}'])
        if montaz:
            cena_data.append(['Montáž', f'{cena_montaz:.2f}'])
        if doprava:
            cena_data.append(['Doprava', f'{cena_doprava:.2f}'])
        if navrh:
            cena_data.append(['Grafický návrh', f'{cena_navrh:.2f}'])
        if priorita == "Expresná":
            cena_data.append(['Expresná priorita', f'{prirazka_priorita:.2f}'])
        cena_data.append(['CELKOM', f'{celkova_cena:.2f}'])
        
        cena_table = Table(cena_data, colWidths=[3*inch, 2*inch])
        cena_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(cena_table)
        
        if poznamky:
            story.append(Spacer(1, 20))
            story.append(Paragraph("POZNÁMKY", styles['Heading2']))
            story.append(Paragraph(poznamky, styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        
        # Download tlačidlo
        st.download_button(
            label="⬇️ Stiahnuť PDF",
            data=buffer,
            file_name=f"ponuka_{nazov_projektu.replace(' ', '_')}_{datum.strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        
        st.success("PDF ponuka bola vygenerovaná!")
    else:
        st.error("Vyplňte prosím názov projektu a zákazníka!") 