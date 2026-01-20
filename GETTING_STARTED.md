# 🚀 Come Iniziare

## Setup Iniziale (già fatto!)

L'ambiente è già configurato con:
- ✅ Python virtual environment (`.venv/`)
- ✅ fpdf2 e Pillow installati
- ✅ Struttura cartelle creata
- ✅ 6 esempi pronti da eseguire

## 📚 Percorso di Apprendimento

### 1️⃣ Inizia dagli Esempi Base

Esegui gli esempi nell'ordine per imparare gradualmente:

```bash
# Attiva l'ambiente virtuale (se non già attivo)
source .venv/bin/activate

# Vai nella cartella examples
cd examples

# Esempio 1: Hello World
python 01_hello_world.py

# Esempio 2: Formattazione testo
python 02_basic_formatting.py

# Esempio 3: Tabelle
python 03_table_example.py

# Esempio 4: Multi-pagina
python 04_multi_page.py

# Esempio 5: Forme e colori
python 05_shapes_and_colors.py

# Esempio 6: Fattura completa
python 06_invoice_example.py
```

### 2️⃣ Sperimenta nel Playground

Apri `practice/playground.py` e inizia a sperimentare:

```bash
cd practice
python playground.py
```

### 3️⃣ Consulta la Guida Rapida

Il file `QUICK_REFERENCE.py` contiene una sintesi di tutti i comandi principali:

```bash
python QUICK_REFERENCE.py  # Stampa la guida
```

## 📖 Studiare la Documentazione

### Tutorial in Italiano
https://py-pdf.github.io/fpdf2/Tutorial-it.html

### Documentazione Completa
https://py-pdf.github.io/fpdf2/

### Sezioni Utili:
- **Tabelle**: https://py-pdf.github.io/fpdf2/Tables.html
- **HTML to PDF**: https://py-pdf.github.io/fpdf2/HTML.html
- **Immagini**: https://py-pdf.github.io/fpdf2/Images.html
- **Unicode/Font**: https://py-pdf.github.io/fpdf2/Unicode.html

## 💡 Tips per Iniziare

1. **Sperimenta modificando gli esempi**
   - Cambia colori, dimensioni, testi
   - Aggiungi nuove sezioni
   - Prova combinazioni diverse

2. **Usa QUICK_REFERENCE.py**
   - Contiene tutti i comandi base
   - Sintassi veloce da copiare

3. **Guarda gli esempi complessi**
   - `06_invoice_example.py` mostra come combinare tutto
   - Studia come è strutturato il codice

4. **Apri i PDF generati**
   - Tutti i PDF vanno in `output/`
   - Apri e verifica il risultato dopo ogni modifica

## 🎯 Primi Esercizi Suggeriti

1. **Crea la tua "business card" in PDF**
   - Nome, ruolo, contatti
   - Logo (box colorato)
   - Layout carino

2. **Report con grafici simulati**
   - Usa rect() e ellipse() per creare "grafici"
   - Tabella con dati
   - Header/footer personalizzati

3. **Certificato/Diploma**
   - Testo grande centrato
   - Bordo decorativo
   - Firma (testo in corsivo)

4. **Menu Ristorante**
   - Sezioni (Antipasti, Primi, etc.)
   - Prezzi allineati a destra
   - Descrizioni piccole sotto il nome del piatto

## 🔧 Comandi Utili

```bash
# Esegui tutti gli esempi in sequenza
python run_all_examples.py

# Installa pacchetti aggiuntivi (se serve)
pip install nome-pacchetto

# Aggiorna fpdf2
pip install --upgrade fpdf2
```

## 📝 Note Importanti

- **Coordinate**: (0,0) è in alto a sinistra
- **Unità**: default sono millimetri
- **Pagina A4**: 210mm × 297mm
- **Font base**: Helvetica, Times, Courier (non servono file font)
- **Euro symbol**: usa "EUR" invece di "€" con font base

## 🐛 Troubleshooting

**Errore Unicode?**
- Usa font standard (Helvetica) con caratteri ASCII
- Per caratteri speciali, usa font TTF Unicode (vedi docs)

**PDF vuoto?**
- Hai chiamato `pdf.output()`?
- Hai aggiunto almeno una pagina con `pdf.add_page()`?

**Testo fuori pagina?**
- Controlla le coordinate x,y
- Usa `pdf.ln()` per andare a capo

---

Buon divertimento con fpdf2! 🎉
