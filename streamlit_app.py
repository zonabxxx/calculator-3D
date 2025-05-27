import streamlit as st
import pandas as pd
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

def create_pdf_with_utf8(nazov_projektu, zakaznik, datum, pocet_pismen, vyska_pismen, material, 
                        zakladna_cena, celkova_cena, lakovanie, foliovanie, osvetlenie, 
                        montaz, doprava, navrh, poznamky, osvetlenie_cena=0):
    """Vytvorenie PDF s podporou UTF-8 a profesionálnym dizajnom"""
    buffer = io.BytesIO()
    
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Registrácia fontu s podporou diakritiky
    try:
        # Pokus o registráciu fontu s UTF-8 podporou
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
                    pdfmetrics.registerFont(TTFont('ArialUTF8', font_path))
                    font_name = 'ArialUTF8'
                    font_bold = 'ArialUTF8'  # Použijeme rovnaký font
                    font_registered = True
                    break
                except:
                    continue
        
        if not font_registered:
            font_name = 'Helvetica'
            font_bold = 'Helvetica-Bold'
    except:
        font_name = 'Helvetica'
        font_bold = 'Helvetica-Bold'
    
    # Funkcia na bezpečné kreslenie textu s diakritiku
    def draw_text_safe(canvas_obj, x, y, text, font='Helvetica', size=10):
        try:
            canvas_obj.setFont(font, size)
            # Konverzia na UTF-8 a spracovanie špeciálnych znakov
            safe_text = str(text).encode('utf-8').decode('utf-8')
            canvas_obj.drawString(x, y, safe_text)
        except:
            # Fallback - nahradenie problematických znakov
            safe_text = str(text).replace('ľ', 'l').replace('š', 's').replace('č', 'c').replace('ť', 't').replace('ž', 'z').replace('ý', 'y').replace('á', 'a').replace('í', 'i').replace('é', 'e').replace('ó', 'o').replace('ú', 'u').replace('ň', 'n').replace('ď', 'd').replace('ô', 'o').replace('ŕ', 'r').replace('ĺ', 'l')
            canvas_obj.setFont('Helvetica', size)
            canvas_obj.drawString(x, y, safe_text)
    
    def draw_text_right_safe(canvas_obj, x, y, text, font='Helvetica', size=10):
        try:
            canvas_obj.setFont(font, size)
            safe_text = str(text).encode('utf-8').decode('utf-8')
            canvas_obj.drawRightString(x, y, safe_text)
        except:
            safe_text = str(text).replace('ľ', 'l').replace('š', 's').replace('č', 'c').replace('ť', 't').replace('ž', 'z').replace('ý', 'y').replace('á', 'a').replace('í', 'i').replace('é', 'e').replace('ó', 'o').replace('ú', 'u').replace('ň', 'n').replace('ď', 'd').replace('ô', 'o').replace('ŕ', 'r').replace('ĺ', 'l')
            canvas_obj.setFont('Helvetica', size)
            canvas_obj.drawRightString(x, y, safe_text)
    
    # === HLAVIČKA S LOGOM A FIRMOU ===
    # Logo obrázok (ľavá strana)
    try:
        logo_path = "grafika /ADSUN-logo-web.jpg"
        logo = ImageReader(logo_path)
        # Vloženie loga - upravená veľkosť pre hlavičku
        c.drawImage(logo, 50, height - 100, width=120, height=40, preserveAspectRatio=True)
        
        # Údaje firmy pod logom
        draw_text_safe(c, 50, height - 110, "AD Sun s.r.o.", font_name, 10)
        draw_text_safe(c, 50, height - 125, "Bratislava 50", font_name, 10)
        draw_text_safe(c, 50, height - 140, "Svetelná reklama republika", font_name, 10)
        draw_text_safe(c, 50, height - 155, "IČO: 36828722", font_name, 10)
        draw_text_safe(c, 50, height - 170, "DIČ: 2022406838", font_name, 10)
        draw_text_safe(c, 50, height - 185, "IČ DPH: SK2022406838", font_name, 10)
        
    except Exception as e:
        # Fallback ak sa logo nenačíta
        draw_text_safe(c, 50, height - 60, "AD SUN", font_bold, 24)
        
        draw_text_safe(c, 50, height - 80, "AD Sun s.r.o.", font_name, 10)
        draw_text_safe(c, 50, height - 95, "Bratislava 50", font_name, 10)
        draw_text_safe(c, 50, height - 110, "Svetelná reklama republika", font_name, 10)
        draw_text_safe(c, 50, height - 125, "IČO: 36828722", font_name, 10)
        draw_text_safe(c, 50, height - 140, "DIČ: 2022406838", font_name, 10)
        draw_text_safe(c, 50, height - 155, "IČ DPH: SK2022406838", font_name, 10)
    
    # Číslo ponuky (pravá strana)
    ponuka_cislo = f"25000{datum.strftime('%m%d')}"
    draw_text_right_safe(c, width - 50, height - 60, f"Cenová ponuka: {ponuka_cislo}", font_bold, 12)
    
    # === ÚDAJE O ZÁKAZNÍKOVI ===
    draw_text_safe(c, 350, height - 120, "Odberateľ:", font_bold, 10)
    draw_text_safe(c, 350, height - 140, zakaznik.upper(), font_name, 10)
    draw_text_safe(c, 350, height - 155, "Slovenská republika", font_name, 10)
    
    # IČO a DIČ zákazníka (ak sú zadané v poznámkach)
    y_customer = height - 175
    if "IČO" in poznamky:
        lines = poznamky.split('\n')
        for line in lines:
            if "IČO" in line or "DIČ" in line:
                draw_text_safe(c, 350, y_customer, line, font_name, 10)
                y_customer -= 15
    
    # Dátum vystavenia
    draw_text_safe(c, 350, y_customer - 20, f"Vystavené: {datum.strftime('%d.%m.%Y')}", font_name, 10)
    
    # === HORIZONTÁLNA ČIARA ===
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(50, height - 220, width - 50, height - 220)
    
    # === TABUĽKA S CENAMI ===
    draw_text_safe(c, 50, height - 250, "Cenová ponuka:", font_bold, 10)
    
    # Hlavička tabuľky
    y_table = height - 280
    c.setFillColor(colors.lightgrey)
    c.rect(50, y_table - 5, 540, 20, fill=1, stroke=1)
    
    c.setFillColor(colors.black)
    draw_text_safe(c, 60, y_table, "Č.", font_bold, 9)
    draw_text_safe(c, 80, y_table, "Položka", font_bold, 9)
    draw_text_safe(c, 350, y_table, "Množstvo", font_bold, 9)
    draw_text_safe(c, 420, y_table, "MJ", font_bold, 9)
    draw_text_safe(c, 450, y_table, "Cena/MJ", font_bold, 9)
    draw_text_safe(c, 520, y_table, "Spolu bez DPH", font_bold, 9)
    
    # Riadky tabuľky
    y_table -= 25
    row_num = 1
    
    # Základné písmená
    draw_text_safe(c, 60, y_table, str(row_num), font_name, 9)
    draw_text_safe(c, 80, y_table, f"Kazetové 3D písmená - {vyska_pismen}", font_name, 9)
    draw_text_safe(c, 80, y_table - 12, f"Materiál: {material}", font_name, 9)
    draw_text_safe(c, 80, y_table - 24, f"Výška písmen: {vyska_pismen}", font_name, 9)
    draw_text_safe(c, 350, y_table, str(pocet_pismen), font_name, 9)
    draw_text_safe(c, 420, y_table, "ks", font_name, 9)
    predajna_cena_na_pismeno = zakladna_cena / pocet_pismen
    draw_text_safe(c, 450, y_table, f"{predajna_cena_na_pismeno:.2f}", font_name, 9)
    draw_text_right_safe(c, 580, y_table, f"{zakladna_cena:.2f}", font_name, 9)
    
    y_table -= 40
    row_num += 1
    
    # Dodatočné služby
    if lakovanie:
        draw_text_safe(c, 60, y_table, str(row_num), font_name, 9)
        draw_text_safe(c, 80, y_table, "Lakovanie", font_name, 9)
        lakovanie_cena = zakladna_cena * 0.15
        draw_text_safe(c, 350, y_table, "1", font_name, 9)
        draw_text_safe(c, 420, y_table, "ks", font_name, 9)
        draw_text_safe(c, 450, y_table, f"{lakovanie_cena:.2f}", font_name, 9)
        draw_text_right_safe(c, 580, y_table, f"{lakovanie_cena:.2f}", font_name, 9)
        y_table -= 25
        row_num += 1
    
    if foliovanie:
        draw_text_safe(c, 60, y_table, str(row_num), font_name, 9)
        draw_text_safe(c, 80, y_table, "Fóliovanie", font_name, 9)
        foliovanie_cena = zakladna_cena * 0.20
        draw_text_safe(c, 350, y_table, "1", font_name, 9)
        draw_text_safe(c, 420, y_table, "ks", font_name, 9)
        draw_text_safe(c, 450, y_table, f"{foliovanie_cena:.2f}", font_name, 9)
        draw_text_right_safe(c, 580, y_table, f"{foliovanie_cena:.2f}", font_name, 9)
        y_table -= 25
        row_num += 1
    
    if osvetlenie:
        draw_text_safe(c, 60, y_table, str(row_num), font_name, 9)
        draw_text_safe(c, 80, y_table, "LED osvetlenie", font_name, 9)
        draw_text_safe(c, 350, y_table, str(pocet_pismen), font_name, 9)
        draw_text_safe(c, 420, y_table, "ks", font_name, 9)
        osvetlenie_za_kus = osvetlenie_cena / pocet_pismen if pocet_pismen > 0 else 0
        draw_text_safe(c, 450, y_table, f"{osvetlenie_za_kus:.2f}", font_name, 9)
        draw_text_right_safe(c, 580, y_table, f"{osvetlenie_cena:.2f}", font_name, 9)
        y_table -= 25
        row_num += 1
    
    if montaz:
        draw_text_safe(c, 60, y_table, str(row_num), font_name, 9)
        draw_text_safe(c, 80, y_table, "Montáž a inštalácia", font_name, 9)
        montaz_cena = zakladna_cena * 0.25
        draw_text_safe(c, 350, y_table, "1", font_name, 9)
        draw_text_safe(c, 420, y_table, "ks", font_name, 9)
        draw_text_safe(c, 450, y_table, f"{montaz_cena:.2f}", font_name, 9)
        draw_text_right_safe(c, 580, y_table, f"{montaz_cena:.2f}", font_name, 9)
        y_table -= 25
        row_num += 1
    
    if doprava:
        draw_text_safe(c, 60, y_table, str(row_num), font_name, 9)
        draw_text_safe(c, 80, y_table, "Doprava", font_name, 9)
        draw_text_safe(c, 350, y_table, "1", font_name, 9)
        draw_text_safe(c, 420, y_table, "ks", font_name, 9)
        draw_text_safe(c, 450, y_table, "50.00", font_name, 9)
        draw_text_right_safe(c, 580, y_table, "50.00", font_name, 9)
        y_table -= 25
        row_num += 1
    
    if navrh:
        draw_text_safe(c, 60, y_table, str(row_num), font_name, 9)
        draw_text_safe(c, 80, y_table, "Grafický návrh", font_name, 9)
        draw_text_safe(c, 350, y_table, "1", font_name, 9)
        draw_text_safe(c, 420, y_table, "ks", font_name, 9)
        draw_text_safe(c, 450, y_table, "100.00", font_name, 9)
        draw_text_right_safe(c, 580, y_table, "100.00", font_name, 9)
        y_table -= 25
    
    # === SÚČTY ===
    y_table -= 20
    c.setLineWidth(1)
    c.line(400, y_table, width - 50, y_table)
    
    y_table -= 20
    draw_text_safe(c, 400, y_table, "Spolu bez DPH:", font_bold, 10)
    draw_text_right_safe(c, 580, y_table, f"{celkova_cena:.2f} €", font_bold, 10)
    
    y_table -= 15
    dph = celkova_cena * 0.23  # 23% DPH
    draw_text_safe(c, 400, y_table, "DPH 23%:", font_bold, 10)
    draw_text_right_safe(c, 580, y_table, f"{dph:.2f} €", font_bold, 10)
    
    y_table -= 15
    celkom_s_dph = celkova_cena + dph
    draw_text_safe(c, 400, y_table, "CELKOM:", font_bold, 12)
    draw_text_right_safe(c, 580, y_table, f"{celkom_s_dph:.2f} €", font_bold, 12)
    
    # === POZNÁMKY ===
    if poznamky:
        y_table -= 40
        draw_text_safe(c, 50, y_table, "Poznámky:", font_bold, 10)
        y_table -= 15
        
        # Rozdelenie poznámok na riadky
        words = poznamky.split(' ')
        line = ""
        for word in words:
            test_line = line + word + " "
            if c.stringWidth(test_line, font_name, 9) < width - 100:
                line = test_line
            else:
                draw_text_safe(c, 50, y_table, line.strip(), font_name, 9)
                y_table -= 12
                line = word + " "
        if line:
            draw_text_safe(c, 50, y_table, line.strip(), font_name, 9)
    
    # === PÄTIČKA ===
    draw_text_safe(c, 50, 50, "Všeobecné podmienky: www.adsun.sk", font_name, 8)
    draw_text_right_safe(c, width - 50, 50, "1 / 2", font_name, 8)
    
    c.save()
    buffer.seek(0)
    return buffer

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
        osvetlenie_cena = 0
        
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
        # Vytvorenie PDF s UTF-8 podporou
        pdf_buffer = create_pdf_with_utf8(
            nazov_projektu, zakaznik, datum, pocet_pismen, vyska_pismen, material,
            zakladna_cena, celkova_cena, lakovanie, foliovanie, osvetlenie,
            montaz, doprava, navrh, poznamky, osvetlenie_cena
        )
        
        # Download tlačidlo
        st.download_button(
            label="⬇️ Stiahnuť PDF",
            data=pdf_buffer,
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