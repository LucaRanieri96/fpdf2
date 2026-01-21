# 📚 Guida alla Componentizzazione PDF Kobak

## 🎯 Filosofia

La libreria `base_pdf.py` offre **componenti riutilizzabili** (mattoncini Lego) per costruire qualsiasi PDF Kobak mantenendo coerenza visiva e riducendo duplicazioni di codice.

---

## 🏗️ Struttura Base

```python
from generators.base_pdf import KobakPDF, COLORS

class MioPDF(KobakPDF):
    """Il tuo PDF personalizzato"""
    
    def __init__(self):
        super().__init__(
            company_name="KOBAK S.r.l.",
            logo_path="path/to/logo.png"  # opzionale
        )
    
    def generate(self, data):
        self.add_page()
        # Componi il PDF con i componenti base
        self.add_document_title("Titolo Documento")
        # ... altri componenti
        self.output("output.pdf")

```

---

## 📦 Componenti Disponibili

### 🎨 **Branding e Layout**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `header()` / `footer()` | Branding automatico su ogni pagina | Ereditato automaticamente |
| `add_line(color, width)` | Linea orizzontale separatrice | `pdf.add_line('primary', 0.5)` |
| `add_spacing(height)` | Spaziatura verticale | `pdf.add_spacing(10)` |
| `rounded_rect(x, y, w, h, r)` | Rettangolo angoli arrotondati | `pdf.rounded_rect(10, 10, 50, 20, 2)` |

### 📝 **Tipografia**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_text(text, style, color, align)` | Testo singola riga/paragrafo | `pdf.add_text("Ciao", style='heading')` |
| `add_paragraph(text, align)` | Paragrafo multi-linea | `pdf.add_paragraph("Lungo testo...")` |
| `add_title(text)` | Titolo centrato con bordo | `pdf.add_title("Contratto 2024")` |
| `add_heading(text)` | Intestazione sezione | `pdf.add_heading("Dettagli Cliente")` |
| `add_section_heading(title)` | Heading con linea sotto | `pdf.add_section_heading("Servizi")` |

### 🏷️ **Header/Chip Colorati**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_document_title(title)` | Barra titolo gialla | `pdf.add_document_title("Fattura")` |
| `add_section_chip(title, variant)` | Chip colorato (oro/grigio) | `pdf.add_section_chip("Info", 'gold')` |
| `add_offer_section_title(title)` | Alias chip | `pdf.add_offer_section_title("Offerta")` |

### 📊 **Tabelle**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_table(data, headers, col_widths, style)` | Tabella semplice/styled | `pdf.add_table(rows, ['Col1', 'Col2'])` |
| `add_zebra_table(headers, rows, ...)` | Tabella zebra striping automatico | `pdf.add_zebra_table(['Nome', 'Età'], data)` |
| `add_items_table(items, headers)` | Tabella articoli (desc, qty, prezzi) | `pdf.add_items_table(service_items)` |
| `add_details_table(rows)` | Tabella dettagliata con zebra | `pdf.add_details_table(details)` |

### 💰 **Totali e Riepilogo**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_totals_section(subtotal, vat, total, vat_rate)` | Box totali a destra | `pdf.add_totals_section("500", "110", "610")` |
| `add_totals_list(totals, highlight_last)` | Lista totali a righe | `pdf.add_totals_list([('Sub', '500'), ('Tot', '610')])` |

### 📋 **Info Card e Griglie**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_info_grid(rows, label_width, line_height)` | **NUOVO** Griglia label/valore | `pdf.add_info_grid([('Nome:', 'Mario'), ('Tel:', '123')])` |
| `add_info_card(title, rows, variant, ...)` | Card con header + righe info | `pdf.add_info_card("Cliente", [('P.IVA', '123')])` |
| `add_labeled_line(label, value)` | Singola riga "Label: Value" | `pdf.add_labeled_line("Data", "20/01/2024")` |

### 📐 **Layout a Colonne**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_columns(texts, ncols, gutter)` | Colonne testo automatiche | `pdf.add_columns(['testo1', 'testo2'], ncols=2)` |
| `add_two_columns_with_callbacks(left_fn, right_fn, ...)` | Colonne con callback | `pdf.add_two_columns_with_callbacks(lambda: ...)` |
| `add_columns_with_headers(...)` | **NUOVO** Colonne con header colorati | Vedi esempio sotto |
| `add_two_column_info_boxes(...)` | **NUOVO** Due box info affiancati | Vedi esempio sotto |

### ✅ **Checkbox e Form**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_checkbox(x, y, size, checked)` | Singolo checkbox | `pdf.add_checkbox(10, 20, 4, checked=True)` |
| `add_checkbox_row(items, spacing, ...)` | Riga checkbox orizzontali | `pdf.add_checkbox_row(['Opt1', 'Opt2'])` |
| `add_form_checkboxes(options, checked_indices, ...)` | **NUOVO** Lista checkbox verticale | `pdf.add_form_checkboxes(['A', 'B', 'C'])` |

### ✍️ **Firma e Termini**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_signature_blocks(blocks, gutter)` | Blocchi firma multipli | `pdf.add_signature_blocks([{'title': 'Firma'}])` |
| `add_contract_terms(clauses)` | Elenco clausole numerate | `pdf.add_contract_terms(['Art 1...', 'Art 2...'])` |

### 🔗 **Link e Badge**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_clickable_link(text, url, page)` | Link esterno/interno | `pdf.add_clickable_link("Sito", url="https://...")` |
| `add_status_badge(text, type)` | Badge colorato (pending/accepted/rejected) | `pdf.add_status_badge("Approvato", 'accepted')` |

### 📄 **Sezioni Documento Predefinite**

| Componente | Uso | Esempio |
|-----------|-----|---------|
| `add_document_info(number, date, label_prefix)` | Box info documento | `pdf.add_document_info("FAT-001", "20/01/2024")` |
| `add_client_info(name, vat, address, ...)` | Box cliente | `pdf.add_client_info("Acme", "IT123...")` |
| `add_validity_info(valid_until, ...)` | Info validità offerta | `pdf.add_validity_info("30/12/2024")` |
| `add_notes_section(notes)` | Sezione note | `pdf.add_notes_section("Note importanti...")` |

---

## 🚀 Componenti Nuovi (Refactoring 2024)

### 1️⃣ `add_info_grid()`
**Elimina** ripetizioni di `set_font` + `cell` per coppie label/valore.

**Prima (codice ripetitivo):**
```python
self.set_font(font, 'B', 7)
self.cell(28, 4, 'Nome:', new_x=XPos.RIGHT)
self.set_font(font, '', 7)
self.cell(width - 28, 4, 'Mario', new_x=XPos.LEFT, new_y=YPos.NEXT)

self.set_font(font, 'B', 7)
self.cell(28, 4, 'Tel.:', new_x=XPos.RIGHT)
self.set_font(font, '', 7)
self.cell(width - 28, 4, '123456', new_x=XPos.LEFT, new_y=YPos.NEXT)
```

**Dopo (componente riutilizzabile):**
```python
self.add_info_grid([
    ('Nome:', 'Mario'),
    ('Tel.:', '123456')
], label_width=28)
```

---

### 2️⃣ `add_form_checkboxes()`
**Semplifica** liste di checkbox verticali.

**Prima:**
```python
y = self.get_y()
self.rounded_rect(self.get_x(), y, 4, 4, 0.5, style='D')
self.set_x(self.get_x() + 6)
self.cell(0, 4, "Opzione 1", new_x=XPos.LEFT, new_y=YPos.NEXT)

y = self.get_y()
self.rounded_rect(self.get_x(), y, 4, 4, 0.5, style='D')
self.set_x(self.get_x() + 6)
self.cell(0, 4, "Opzione 2", new_x=XPos.LEFT, new_y=YPos.NEXT)
```

**Dopo:**
```python
self.add_form_checkboxes([
    "Opzione 1",
    "Opzione 2",
    "Opzione 3"
], checked_indices=[0])  # Prima checkbox selezionata
```

---

### 3️⃣ `add_two_column_info_boxes()`
**Combina** layout a due colonne + header + info grid.

**Prima (50+ righe manuali):**
```python
# Calcoli manuali coordinate
y_start = self.get_y()
x_left = self.l_margin
col_width = (self.w - margins) * 0.5
x_right = x_left + col_width + gutter

# Colonna sinistra
self.set_xy(x_left, y_start)
self.add_section_header("DATI CLIENTE", width=col_width)
for label, value in cliente:
    self.set_x(x_left)
    self.set_font(font, 'B', 7)
    self.cell(28, 4, label, new_x=XPos.RIGHT)
    # ... 20 righe di ripetizioni

# Colonna destra
self.set_xy(x_right, y_start)
self.add_gray_header("SEDE", width=col_width)
for label, value in sede:
    # ... altre 20 righe
```

**Dopo:**
```python
self.add_two_column_info_boxes(
    left_header='DATI CLIENTE',
    left_rows=[('Nome:', 'Acme'), ('P.IVA:', 'IT123...')],
    right_header='SEDE',
    right_rows=[('Indirizzo:', 'Via Roma 1')],
    left_header_bg='primary',
    right_header_bg='chip_gray'
)
```

---

### 4️⃣ `add_zebra_table()`
**Automatizza** striping alternato + header styled.

**Prima:**
```python
# Header
self.add_table_row_with_fill(
    cells=headers,
    widths=[...],
    fill=True,
    fill_color=(246, 246, 246),
    font_style='B',
    # ... 5 parametri
)

# Rows con loop manuale
for idx, row in enumerate(data):
    color = (249, 249, 249) if idx % 2 == 0 else (255, 255, 255)
    self.add_table_row_with_fill(
        cells=row,
        widths=[...],
        fill=True,
        fill_color=color,
        # ... altri parametri
    )
```

**Dopo:**
```python
self.add_zebra_table(
    headers=['Descrizione', 'Quantità', 'Prezzo'],
    rows=data,
    col_widths=[0.6, 0.2, 0.2],
    aligns=['L', 'C', 'R']
)
```

---

## 🔧 Pattern di Composizione

### Esempio 1: Fattura/Preventivo
```python
class InvoicePDF(KobakPDF):
    def generate(self, data):
        self.add_page()
        
        # 1. Titolo documento
        self.add_document_title("FATTURA")
        
        # 2. Info documento + cliente (affiancati)
        info_y, h, col_w, gutter = self.add_document_info(
            data['invoice_number'], data['date'], "Fattura"
        )
        self.add_client_info(
            data['client_name'], data['client_vat'],
            anchor_y=info_y, col_width=col_w, gutter=gutter
        )
        
        # 3. Tabella articoli
        self.add_items_table(data['items'])
        
        # 4. Totali
        self.add_totals_section(
            data['subtotal'], data['vat'], data['total']
        )
        
        # 5. Note
        self.add_notes_section(data['notes'])
        
        self.output("fattura.pdf")
```

### Esempio 2: Contratto (refactored)
```python
class ContractPDF(KobakPDF):
    def generate(self, data):
        self.add_page()
        
        # 1. Offerta
        self.add_section_header("OFFERTA")
        self.add_info_grid([
            ('Offerta n.', data['order_number']),
            ('Validità gg:', data['validity_days'])
        ])
        
        # 2. Cliente + Sede (componente nuovo!)
        self.add_two_column_info_boxes(
            left_header='DATI CLIENTE',
            left_rows=[(k, v) for k, v in data['client'].items()],
            right_header='SEDE POSTA',
            right_rows=[(k, v) for k, v in data['post_office'].items()]
        )
        
        # 3. Checkbox fatture (componente nuovo!)
        self.add_gray_header("SPEDIZIONE FATTURE")
        self.add_form_checkboxes([
            "Solo Fattura Elettronica",
            "Anche Posta Cartacea"
        ])
        
        # 4. Tabella servizi (componente migliorato!)
        self.add_section_header("SERVIZI")
        self.add_zebra_table(
            headers=['DESCRIZIONE', 'QTÀ', 'PREZZO'],
            rows=data['services']
        )
        
        # 5. Totali
        self.add_totals_section(data['subtotal'], data['vat'], data['total'])
        
        # 6. Firme
        self.add_signature_blocks(data['signature_blocks'])
        
        self.output("contratto.pdf")
```

---

## 📊 Vantaggi del Refactoring

| **Prima** | **Dopo** |
|-----------|----------|
| 50+ righe per sezione cliente | 5 righe con `add_two_column_info_boxes` |
| 15+ righe per checkbox | 3 righe con `add_form_checkboxes` |
| 30+ righe per tabella zebra | 5 righe con `add_zebra_table` |
| Calcoli coordinate manuali | Automatico con callback/colonne |
| Codice duplicato in ogni PDF | Componenti riutilizzabili in `base_pdf.py` |

---

## 🎨 Palette Colori Kobak

```python
COLORS = {
    'primary': (249, 221, 0),           # Giallo Kobak
    'primary_dark': (227, 201, 0),      # Giallo scuro
    'primary_light': (250, 228, 51),    # Giallo chiaro
    
    'secondary': (139, 139, 135),       # Grigio Kobak
    'secondary_dark': (76, 75, 72),     # Grigio scuro
    'secondary_light': (204, 204, 199), # Grigio chiaro
    
    'chip_gray': (119, 119, 119),       # Chip grigio
    'chip_gray_light': (240, 240, 240), # Chip grigio chiaro
    
    'bg_light': (246, 246, 246),        # Background chiaro
    'bg_white': (255, 255, 255),        # Bianco
    
    'text_dark': (37, 36, 32),          # Testo scuro
    'text_light': (180, 180, 176),      # Testo chiaro
    'text_white': (255, 255, 255),      # Testo bianco
    
    'status_pending': (245, 158, 11),   # Arancione (in attesa)
    'status_accepted': (16, 185, 129),  # Verde (accettato)
    'status_rejected': (239, 68, 68),   # Rosso (rifiutato)
}
```

**Uso:**
```python
self.set_fill_color(*COLORS['primary'])
self.add_status_badge("Approvato", 'accepted')
```

---

## 📐 Font Standard Kobak

```python
FONT_CONFIG = {
    'title': {'size': 20, 'height': 24, 'style': 'B'},
    'subtitle': {'size': 15, 'height': 18, 'style': 'B'},
    'heading': {'size': 13, 'height': 16, 'style': 'B'},
    'body': {'size': 11, 'height': 13, 'style': ''},
    'small': {'size': 9, 'height': 11, 'style': 'I'},
}
```

**Uso:**
```python
self.add_text("Titolo", style='title')
self.add_text("Corpo", style='body')
```

---

## 🧪 Testing

Testa il tuo PDF:
```bash
cd /home/lucar/Desktop/fpdf2
python generators/kobak_contract_pdf.py
```

Genera: `contratto_kobak_esempio.pdf` con:
- ✅ Layout a colonne automatico
- ✅ Tabelle zebra
- ✅ Checkbox form
- ✅ Info grid senza ripetizioni
- ✅ Branding Kobak coerente

---

## 🎓 Best Practices

1. **Riusa componenti base** invece di scrivere codice custom
2. **Usa wrapper legacy** (es. `add_section_header`) per compatibilità
3. **Preferisci callback** (`add_two_columns_with_callbacks`) per layout complessi
4. **Mantieni coerenza** con palette/font Kobak
5. **Testa sempre** il PDF generato per verificare layout

---

## 🔮 Prossimi Passi

Per creare un nuovo PDF:
1. Eredita da `KobakPDF`
2. Componi con i componenti base
3. Override `header()`/`footer()` se serve branding custom
4. Testa con dati reali

**Happy PDF Generation! 🎉**
