# Componentizzazione PDF Kobak

## 📐 Architettura

Il sistema PDF Kobak è ora organizzato in **componenti riutilizzabili** seguendo il pattern di composizione.

```
generators/
├── base_pdf.py          # ← Classe base con tutti i componenti
└── kobak_contract_pdf.py # ← Contratti specifici (eredita da base)
```

---

## 🧱 Componenti Base (`base_pdf.py`)

La classe `KobakPDF` fornisce mattoncini riutilizzabili divisi per categoria:

### **1. Componenti Forme**
```python
# Rettangolo arrotondato
pdf.rounded_rect(x, y, width, height, radius, style='F')

# Linea orizzontale
pdf.draw_horizontal_line(color=COLORS['primary'], width=0.5)
```

### **2. Componenti Testo**
```python
# Label: Value
pdf.add_label_value_line(
    label="Cliente:", 
    value="Mario Rossi",
    label_width=40,
    font_size=7
)

# Blocco testo
pdf.add_text_block("Lorem ipsum...", font_size=8, align='J')
```

### **3. Componenti Layout**
```python
# Due colonne con callback
pdf.add_two_columns_with_callbacks(
    left_fn=lambda: pdf.add_text("Sinistra"),
    right_fn=lambda: pdf.add_text("Destra"),
    col_ratio=0.5
)

# Due colonne con header
pdf.add_columns_with_headers(
    left_header="CLIENTE",
    left_fn=content_fn,
    right_header="SEDE",
    right_fn=content_fn,
    left_header_bg='primary',
    right_header_bg='chip_gray'
)
```

### **4. Componenti Interattivi**
```python
# Singolo checkbox
pdf.add_checkbox(x=10, y=20, size=4, checked=True)

# Riga di checkbox
pdf.add_checkbox_row(
    items=['Email', 'Posta', 'PEC'],
    spacing=10
)

# Con checkbox selezionati
pdf.add_checkbox_row(
    items=[('Email', True), ('Posta', False)],
)
```

### **5. Componenti Tabelle**
```python
# Riga tabella personalizzata
pdf.add_table_row_with_fill(
    cells=['A', 'B', 'C'],
    widths=[0.33, 0.33, 0.34],  # percentuali
    height=5,
    fill=True,
    corner_radius=1
)

# Tabella zebrata completa (già esistente)
pdf.add_zebra_table(headers, rows, col_widths)
```

### **6. Utilità**
```python
# Reset posizione X al margine sinistro
pdf.reset_x()

# Larghezza utile pagina
width = pdf.get_page_width()

# Spazio verticale
pdf.add_spacing(10)
```

---

## 🎨 Palette Colori (`COLORS`)

Tutti i componenti usano la stessa palette:

```python
from generators.base_pdf import COLORS

COLORS['primary']           # Giallo Kobak
COLORS['chip_gray']        # Grigio
COLORS['bg_light']         # Background chiaro
COLORS['text_dark']        # Testo scuro
COLORS['text_white']       # Testo bianco
COLORS['bg_white']         # Bianco
```

---

## 📄 Esempio: Creare un Nuovo PDF

```python
from generators.base_pdf import KobakPDF, COLORS

class MyCustomPDF(KobakPDF):
    def __init__(self):
        super().__init__(
            font='Helvetica',
            company_name="KOBAK S.r.l."
        )
    
    def header(self):
        # Usa componenti base
        self.set_font(self.font_family, 'B', 14)
        self.cell(0, 8, "MY CUSTOM PDF", align='C')
        self.draw_horizontal_line(color=COLORS['primary'])
    
    def generate_document(self):
        self.add_page()
        
        # Intestazione sezione (componente già esistente)
        self.add_section_chip("SEZIONE 1", variant='gold')
        
        # Info a due colonne (nuovo componente)
        def left_content():
            self.add_label_value_line("Nome:", "Mario")
            self.add_label_value_line("Cognome:", "Rossi")
        
        def right_content():
            self.add_label_value_line("Email:", "mario@test.com")
        
        self.add_columns_with_headers(
            "ANAGRAFICA", left_content,
            "CONTATTI", right_content
        )
        
        # Checkbox
        self.add_checkbox_row(['Opzione A', 'Opzione B'])
        
        # Salva
        self.output("my_custom.pdf")

# Usa
pdf = MyCustomPDF()
pdf.generate_document()
```

---

## ✅ Vantaggi della Componentizzazione

1. **Riutilizzo**: Un componente scritto una volta, usato ovunque
2. **Consistenza**: Stesso stile in tutti i PDF
3. **Manutenibilità**: Modifichi un componente → aggiorna tutti i PDF
4. **Leggibilità**: Codice più pulito e dichiarativo
5. **Testabilità**: Ogni componente può essere testato singolarmente

### Prima (senza componenti):
```python
# 20 righe di codice per ogni riga label-value
self.set_x(self.l_margin)
self.set_font(self.font_family, 'B', 7)
self.cell(40, 4, "Cliente:", new_x=XPos.RIGHT)
self.set_font(self.font_family, '', 7)
self.cell(page_width - 40, 4, "Mario Rossi", new_x=XPos.LEFT, new_y=YPos.NEXT)
```

### Dopo (con componenti):
```python
# 1 riga
self.add_label_value_line("Cliente:", "Mario Rossi")
```

---

## 🔄 Migrazione Esistente

Il `kobak_contract_pdf.py` ora:
- **Eredita** da `KobakPDF` invece di `FPDF`
- **Usa componenti base** per funzionalità comuni
- **Mantiene solo logica specifica** del contratto

```python
class KobakContractPDF(KobakPDF):  # ← Eredita da base
    def add_info_line(self, label, value):
        # Delega al componente base
        self.add_label_value_line(label, value, font_size=7)
    
    def add_services_table(self, data):
        # Logica specifica del contratto
        ...
```

---

## 🚀 Prossimi Passi

Per creare un nuovo tipo di PDF (preventivo, fattura, report):

1. Crea nuovo file in `generators/my_new_pdf.py`
2. Eredita da `KobakPDF`
3. Usa i componenti base
4. Aggiungi solo logica specifica

```python
from generators.base_pdf import KobakPDF, COLORS

class MyNewPDF(KobakPDF):
    def generate(self, data):
        self.add_page()
        self.add_section_chip("TITOLO")
        self.add_label_value_line("Campo:", data['value'])
        # ...
```

Tutti i PDF avranno lo stesso stile Kobak automaticamente! 🎨
