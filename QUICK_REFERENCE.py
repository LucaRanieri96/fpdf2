"""
GUIDA RAPIDA FPDF2
==================

## Concetti Base

### 1. Creare un PDF
```python
from fpdf import FPDF

pdf = FPDF()           # Crea oggetto PDF
pdf.add_page()         # Aggiungi pagina
pdf.set_font('Helvetica', size=12)  # Imposta font
pdf.cell(text="Ciao!")  # Aggiungi testo
pdf.output("file.pdf")  # Salva
```

### 2. Font
- Famiglie: 'Helvetica', 'Times', 'Courier'
- Stili: '' (normale), 'B' (bold), 'I' (italic), 'BI' (bold+italic)
- Esempio: pdf.set_font('Helvetica', 'B', 16)

### 3. Colori
- RGB: valori da 0 a 255
- Testo: pdf.set_text_color(r, g, b)
- Riempimento: pdf.set_fill_color(r, g, b)
- Bordi: pdf.set_draw_color(r, g, b)

### 4. Celle (cell)
```python
pdf.cell(
    width=40,           # Larghezza (0 = full width)
    height=10,          # Altezza
    text="Testo",       # Contenuto
    border=0,           # Bordo (0=no, 1=sì)
    align='L',          # Allineamento: L, C, R
    fill=False,         # Riempimento
    new_x="RIGHT",      # Dove posizionare cursore dopo (RIGHT, LMARGIN)
    new_y="TOP"         # Verticale (TOP, NEXT, LAST)
)
```

### 5. Multi-celle (multi_cell)
Per testo lungo che va a capo automaticamente
```python
pdf.multi_cell(
    width=0,            # 0 = usa tutta la larghezza disponibile
    height=5,           # Altezza di ogni riga
    text="Testo lungo..."
)
```

### 6. Forme
```python
# Linea
pdf.line(x1, y1, x2, y2)

# Rettangolo
pdf.rect(x, y, w, h, style='D')  # D=bordo, F=fill, DF=entrambi

# Cerchio/Ellisse
pdf.ellipse(x, y, w, h, style='D')
```

### 7. Posizionamento
```python
pdf.set_xy(x, y)     # Imposta posizione assoluta
pdf.set_x(x)         # Solo x
pdf.set_y(y)         # Solo y
pdf.ln(h)            # Vai a capo (new line)
```

### 8. Pagine
```python
pdf.add_page()                    # Nuova pagina
pdf.add_page(orientation='L')    # Landscape
pdf.page_no()                     # Numero pagina corrente
```

### 9. Header e Footer Personalizzati
```python
class MyPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'Titolo', align='C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Pag {self.page_no()}', align='C')
```

### 10. Tabelle
```python
# Intestazione
pdf.cell(50, 10, 'Col1', border=1)
pdf.cell(50, 10, 'Col2', border=1, new_x="LMARGIN", new_y="NEXT")

# Righe
for row in data:
    pdf.cell(50, 10, row[0], border=1)
    pdf.cell(50, 10, row[1], border=1, new_x="LMARGIN", new_y="NEXT")
```

### 11. Immagini
```python
pdf.image('path/to/image.png', x=10, y=10, w=50)
```

## Coordinate
- Origine (0,0) = angolo in alto a sinistra
- Unità default: millimetri
- Pagina A4: 210mm x 297mm

## Tips Utili
1. Usa new_x="LMARGIN", new_y="NEXT" per andare a capo dopo una cell
2. width=0 nelle celle = usa tutta la larghezza disponibile
3. pdf.ln(h) per aggiungere spazio verticale
4. pdf.alias_nb_pages() per usare {{nb}} = totale pagine

## Link Utili
- Docs: https://py-pdf.github.io/fpdf2/
- Tutorial IT: https://py-pdf.github.io/fpdf2/Tutorial-it.html
- Esempi HTML: https://py-pdf.github.io/fpdf2/HTML.html
- Tabelle avanzate: https://py-pdf.github.io/fpdf2/Tables.html
"""

if __name__ == "__main__":
    print(__doc__)
