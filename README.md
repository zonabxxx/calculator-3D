# 💡 Kalkulátor svetelných reklám

Webová aplikácia pre kalkuláciu cien svetelných reklám s možnosťou generovania PDF ponúk.

## Funkcie

- **3 typy svetelných reklám**: LED panel, Neonová reklama, Svetelný box
- **Inteligentná kalkulácia**: Automatické prepočty podľa špecifikácií
- **PDF export**: Profesionálne ponuky vo formáte PDF
- **Responzívny dizajn**: Funguje na všetkých zariadeniach

## Typy reklám a špecifikácie

### 1. LED panel
- Rozlíšenie: P2.5 - P10
- Jas: 1000-10000 nits
- Umiestnenie: Vnútorné/Vonkajšie
- Farebnosť: Plnofarebný/Jednofarebný/Dvojfarebný

### 2. Neonová reklama
- Typ: Klasický neón/LED neón/EL wire
- Farby: Červená, Modrá, Zelená, Žltá, Biela, RGB
- Hrúbka: 8-18mm
- Tvar: Rovný/Zakrivený/Komplexný

### 3. Svetelný box
- Materiál: Akrylát/Polykarbonát/Plexisklo
- Osvetlenie: LED pásy/Neónové trubice/Halogénové
- Hrúbka: 3-10mm
- Typ: Jednostranné/Obojstranné

## Inštalácia a spustenie

1. **Nainštalujte Python** (verzia 3.8 alebo vyššia)

2. **Nainštalujte závislosti**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Spustite aplikáciu**:
   ```bash
   streamlit run app.py
   ```

4. **Otvorte v prehliadači**: http://localhost:8501

## Použitie

1. **Vyberte typ reklamy** v bočnom menu
2. **Vyplňte základné údaje** (názov projektu, zákazník)
3. **Zadajte rozmery** v centimetrách
4. **Nastavte špecifikácie** podľa typu reklamy
5. **Vyberte dodatočné služby** (montáž, doprava, návrh)
6. **Sledujte kalkuláciu** v reálnom čase
7. **Vygenerujte PDF ponuku** tlačidlom

## Cenník (ukážkové ceny v €/m²)

### LED panely
- P2.5: 800 €/m²
- P3: 600 €/m²
- P4: 450 €/m²
- P5: 350 €/m²
- P6: 280 €/m²
- P8: 200 €/m²
- P10: 150 €/m²

### Neonové reklamy
- Klasický neón: 120 €/m²
- LED neón: 80 €/m²
- EL wire: 40 €/m²

### Svetelné boxy
- LED pásy: 150 €/m²
- Neónové trubice: 100 €/m²
- Halogénové: 80 €/m²

## Prirážky

- **Vonkajšie LED panely**: +30%
- **Plnofarebné LED**: +50%
- **Dvojfarebné LED**: +20%
- **Komplexný tvar neónu**: +80%
- **Zakrivený tvar neónu**: +30%
- **Obojstranný svetelný box**: +60%
- **Montáž**: +15% zo základnej ceny
- **Doprava**: 50 €
- **Grafický návrh**: 100 €
- **Expresná priorita**: +25%

## Prispôsobenie

Ceny a koeficienty môžete jednoducho upraviť v súbore `app.py` v sekcii `zakladne_ceny` a pri výpočte prirážok.

## Podpora

Pre technickú podporu alebo úpravy kontaktujte vývojára. 