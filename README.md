# Kobak PDF Generator

Libreria componibile per generare PDF professionali con stile Kobak consistente.

## 🎯 Caratteristiche

- **Componenti riutilizzabili** - Mattoncini pronti all'uso per costruire PDF
- **Stile consistente** - Palette colori e font Kobak uniformi
- **Estendibile** - Facile creare nuovi tipi di documenti
- **Type-safe** - Completamente tipizzato

## 📦 Setup

```bash
# Crea ambiente virtuale
python3 -m venv .venv

# Attiva ambiente virtuale
source .venv/bin/activate  # Linux/Mac

# Installa dipendenze
pip install -r requirements.txt
```

## 🏗️ Struttura

```
generators/
├── base_pdf.py           # Componenti base riutilizzabili
├── kobak_contract_pdf.py # Generatore contratti
└── __init__.py
```

## 🚀 Quick Start

```python
from generators.base_pdf import KobakPDF, COLORS

# Crea PDF con componenti base
pdf = KobakPDF()
pdf.add_page()

# Usa i componenti
pdf.add_section_chip("TITOLO", variant='gold')
pdf.add_label_value_line("Cliente:", "Mario Rossi")
pdf.add_checkbox_row(['Opzione A', 'Opzione B'])

pdf.output("documento.pdf")
```

### Esempio Contratto

```python
from generators.kobak_contract_pdf import create_sample_contract

# Genera contratto di esempio
output_path = create_sample_contract()
print(f"✓ Contratto generato: {output_path}")
```

## 📚 Documentazione

- [**COMPONENTIZZAZIONE.md**](COMPONENTIZZAZIONE.md) - Guida completa ai componenti
- [fpdf2 Docs](https://py-pdf.github.io/fpdf2/) - Documentazione libreria base

## 🎨 Componenti Disponibili

Vedi [COMPONENTIZZAZIONE.md](COMPONENTIZZAZIONE.md) per la lista completa.

### Esempi:
- `rounded_rect()` - Rettangoli con angoli arrotondati
- `add_label_value_line()` - Righe label-value
- `add_columns_with_headers()` - Layout a colonne con intestazioni
- `add_checkbox_row()` - Checkbox interattivi
- `add_zebra_table()` - Tabelle con righe alternate

## 🔧 Creare Nuovi Documenti

```python
from generators.base_pdf import KobakPDF, COLORS

class MyDocumentPDF(KobakPDF):
    def generate(self, data):
        self.add_page()
        self.add_section_chip("MY DOCUMENT")
        
        # Usa componenti base
        self.add_label_value_line("Campo:", data['value'])
        
        self.output("my_document.pdf")
```

Tutti i documenti avranno automaticamente lo stile Kobak! 🎨
- Tutorial Italiano: https://py-pdf.github.io/fpdf2/Tutorial-it.html
