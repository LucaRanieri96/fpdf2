# 📦 Componenti Standard KobakPDF

Questa è la **libreria di mattoncini** per costruire PDF Kobak.  
Ogni componente ha uno stile standard e uniforme.

## 🧱 Componenti Disponibili

### 1. Header e Footer
Automatici su ogni pagina. Non serve chiamarli.

---

### 2. `add_document_title(title: str)`
**Uso**: Titolo principale del documento  
**Esempio**: `FATTURA`, `PREVENTIVO`, `REPORT`

```python
pdf.add_document_title('FATTURA COMMERCIALE')
```

---

### 3. `add_document_info(number: str, date: str, label_prefix: str = "Documento")`
**Uso**: Box con numero e data del documento  
**Posizione**: Colonna sinistra

```python
pdf.add_document_info(
    number='FAT-2026-001',
    date='20/01/2026',
    label_prefix="Fattura"
)
```

---

### 4. `add_client_info(client_name: str, vat_number: str, address: str = None)`
**Uso**: Box con dati del cliente  
**Posizione**: Colonna destra (si allinea automaticamente con document_info)

```python
pdf.add_client_info(
    client_name='Acme Corporation',
    vat_number='IT12345678901',
    address='Via Roma 123, 10100 Torino'  # Optional
)
```

---

### 5. `add_items_table(items: List[Dict], headers: List[str] = None)`
**Uso**: Tabella articoli standard Kobak  
**Header default**: `['Descrizione', 'Q.ta', 'Prezzo Unit.', 'Importo']`

```python
items = [
    {'description': 'Prodotto A', 'qty': 1, 'unit_price': 'EUR 500,00', 'total': 'EUR 500,00'},
    {'description': 'Prodotto B', 'qty': 2, 'unit_price': 'EUR 300,00', 'total': 'EUR 300,00'},
]

pdf.add_items_table(items)
# Oppure con header personalizzati:
pdf.add_items_table(items, headers=['Desc', 'Q', 'Prezzo', 'Tot'])
```

---

### 6. `add_totals_section(subtotal: str, vat: str, total: str, vat_rate: str = "22%")`
**Uso**: Sezione totali standard  
**Posizione**: Sempre allineata a destra

```python
pdf.add_totals_section(
    subtotal='EUR 1.000,00',
    vat='EUR 220,00',
    total='EUR 1.220,00',
    vat_rate='22%'
)
```

---

### 7. `add_notes_section(notes: str)`
**Uso**: Sezione note finali

```python
pdf.add_notes_section('Pagamento entro 30 giorni. Grazie!')
```

---

### 8. `add_validity_info(valid_until: str)`
**Uso**: Info validità (per preventivi)  
**Posizione**: Sotto client_info

```python
pdf.add_validity_info('20/02/2026')
```

---

### 9. `add_section_heading(title: str)`
**Uso**: Intestazione sezione

```python
pdf.add_section_heading('Articoli')
```

---

### 10. `add_spacing(height: int = 5)`
**Uso**: Spazio verticale

```python
pdf.add_spacing(10)  # 10mm di spazio
```

---

### 11. `add_line(color: str = 'primary', width: float = 0.5)`
**Uso**: Linea orizzontale separatrice

```python
pdf.add_line()                    # Linea gialla
pdf.add_line(color='secondary')   # Linea grigia
```

---

### 12. `add_section_chip(title: str, variant: Literal['gold','gray'] = 'gold')`
**Uso**: Fascia colorata a tutta larghezza per le intestazioni principali (es. OFFERTA, SERVIZI OFFERTI).

```python
pdf.add_section_chip('OFFERTA')
pdf.add_section_chip('TRACCIABILITA', variant='gray')
```

---

### 13. `add_info_card(title: Optional[str], rows: List[Tuple[str, str]], variant: Literal['gold','gray'] = 'gold')`
**Uso**: Box strutturato con intestazione colorata e coppie etichetta/valore (dati cliente, sede di posta, banca, ecc.).

```python
rows = [
    ('Azienda', 'KOBAK France SARL'),
            ('Indirizzo', '66 Avenue des Champs-Elysees, Paris'),
]
pdf.add_info_card('DATI DEL CLIENTE', rows)
```

---

### 14. `add_details_table(rows: List[Dict])`
**Uso**: Tabella servizi dettagliata con 5 colonne, zebra rows e bordo completo.

```python
rows = [
    {
        'description': 'Noleggio bagni chimici',
        'quantity': 10,
        'unit': 'pz',
        'unit_price': 'EUR 150,00',
        'total_price': 'EUR 1.500,00',
    }
]
pdf.add_details_table(rows)
```

---

### 15. `add_totals_list(totals: List[Tuple[str, str]], highlight_last: bool = True)`
**Uso**: Elenco totali a due colonne con riga finale evidenziata.

```python
pdf.add_totals_list([
    ('TOT. IMPONIBILE', 'EUR 2.750,00'),
    ('FURTI/ATTI VANDALICI (5%)', 'EUR 137,50'),
    ('IVA (22%)', 'EUR 635,35'),
    ('TOTALE COMPLESSIVO', 'EUR 3.522,85'),
])
```

---

### 16. `add_signature_blocks(blocks: List[Dict])`
**Uso**: Box affiancati per “Per Accettazione” / “Per Disdetta” con istruzioni e area firma.

```python
blocks = [
    {'title': 'Per Accettazione', 'instructions': 'Luogo ....... Data ......./....../..............'},
    {'title': 'Per Disdetta', 'instructions': 'Ritirare i bagni dal ......./....../..............'},
]
pdf.add_signature_blocks(blocks)
```

---

### 17. `add_contract_terms(clauses: List[str])`
**Uso**: Stampa elenco numerato di clausole contrattuali in corpo ridotto.

```python
pdf.add_contract_terms([
    'Il contratto comprende consegna, manutenzione e ritiro.',
    "Il cliente deve garantire l'accesso ai mezzi Kobak.",
])
```

---

## 📝 Esempio Completo: Fattura

```python
from generators.base_pdf import KobakPDF

pdf = KobakPDF(company_name='KOBAK S.r.l.')
pdf.alias_nb_pages()
pdf.add_page()

# Titolo
pdf.add_document_title('FATTURA COMMERCIALE')
pdf.add_spacing(3)

# Info documento + cliente
pdf.add_document_info(number='FAT-2026-001', date='20/01/2026')
pdf.add_client_info(client_name='Acme Corp', vat_number='IT12345678901')

pdf.add_spacing(5)
pdf.add_line()
pdf.add_spacing(3)

# Articoli
pdf.add_section_heading('Articoli')
items = [
    {'description': 'Prodotto A', 'qty': 1, 'unit_price': 'EUR 500,00', 'total': 'EUR 500,00'},
]
pdf.add_items_table(items)

# Totali
pdf.add_totals_section(
    subtotal='EUR 500,00',
    vat='EUR 110,00',
    total='EUR 610,00'
)

# Note
pdf.add_notes_section('Pagamento entro 30 giorni.')

pdf.output('fattura.pdf')
```

---

## 📝 Esempio Completo: Offerta

```python
from generators.offer_generator import OfferGenerator

offer = {
    'number': 'OFF-0032',
    'office': 'Paris',
    'offer_date': '20/01/2026',
    'validity_days': 30,
    'client': {
        'company': 'ACME Construction',
        'address': '66 Avenue des Champs-Elysees',
        'postal_code': '75008',
        'city': 'Paris',
        'phone': '+33 1 84 74 62 87',
        'vat_number': 'FR123456789',
    },
    'post_office': {'address': 'Rue du Louvre 10, 75001 Paris'},
    'invoice_delivery': {'only_e_invoice': True, 'paper_mail': False, 'email': 'accounting@acme.fr'},
    'service_executor': {
        'company': 'KOBAK France SARL',
        'address': '66 Avenue des Champs-Elysees',
        'city': 'Paris',
        'phone': '0184746287',
    },
    'service_location': {
        'place': 'Chantier Linea 4 Metro',
        'address': 'Rue de Vaugirard 105',
        'manager': 'Ing. Luca Rossi',
    },
    'items': [
        {'description': 'Noleggio bagni', 'quantity': 10, 'unit': 'pz', 'unit_price': 'EUR 150,00', 'total_price': 'EUR 1.500,00'},
    ],
    'totals': {
        'subtotal': 'EUR 2.750,00',
        'risk_label': 'Furti, Incendi e Atti Vandalici (5%)',
        'risk_amount': 'EUR 137,50',
        'tax_label': 'IVA (22%)',
        'tax_amount': 'EUR 635,35',
        'grand_total': 'EUR 3.522,85',
    },
    'payment': {'method': 'Bonifico bancario 30 giorni data fattura'},
    'bank': {
        'name': 'BNP Paribas',
        'branch': 'Paris',
        'iban': 'FR76 1234 5678 9000 1234 5678 901',
        'abi': '12345',
        'cab': '67890',
    },
    'signature_blocks': [
        {'title': 'Per Accettazione', 'instructions': 'Luogo ....... Data ......./....../..............'},
        {'title': 'Per Disdetta', 'instructions': 'Ritirare i bagni dal ......./....../..............'},
    ],
    'terms': ['Il contratto comprende consegna, manutenzione e ritiro.'],
}

pdf = OfferGenerator(
    company_name='KOBAK France SARL',
    company_info=[
        'KOBAK FRANCE SARL - 66 Avenue des Champs-Elysees - 75008 Paris',
        'Telephone: 0184746287 - Mail: info@kobakfrance.fr',
    ],
)
pdf.generate(offer, 'offer_details_32.pdf')
```

---

## 🎨 Palette Colori

Tutti i componenti usano la palette Kobak:

- **Primary**: Giallo `#f9dd00` (227, 221, 0)
- **Secondary**: Grigio `#8b8b87` (139, 139, 135)
- **Text Dark**: `#252420` (37, 36, 32)
- **BG Light**: `#f6f6f6` (246, 246, 246)

---

## 🏗️ Come Creare un Nuovo Tipo di Documento

1. Crea un nuovo generator (es. `contract_generator.py`)
2. Estendi `KobakPDF`
3. Usa i componenti standard nel metodo `generate()`

```python
from generators.base_pdf import KobakPDF

class ContractGenerator(KobakPDF):
    def generate(self, contract_data: dict, output_path: str):
        self.alias_nb_pages()
        self.add_page()
        
        # Usa i mattoncini standard
        self.add_document_title('CONTRATTO')
        self.add_document_info(...)
        self.add_client_info(...)
        # ... altri componenti
        
        self.output(output_path)
```

---

## ✅ Vantaggi di Questa Struttura

✅ **Coerenza**: Tutti i PDF hanno lo stesso aspetto  
✅ **Manutenibilità**: Cambi uno stile, cambia ovunque  
✅ **Documentazione**: Questa guida è la tua reference  
✅ **Velocità**: Crei nuovi PDF in pochi minuti  
✅ **Riutilizzo**: I componenti sono testati e pronti  

---

## 🚀 Nel Backend

```python
# Nel tuo backend Kobak
from generators.invoice_generator import InvoiceGenerator

# Converti i tuoi dati
data = {
    'number': invoice.number,
    'date': invoice.date.strftime('%d/%m/%Y'),
    'customer_name': invoice.customer.name,
    'vat_number': invoice.customer.vat_number,
    'items': [
        {
            'description': item.description,
            'qty': item.quantity,
            'unit_price': f'EUR {item.unit_price:.2f}',
            'total': f'EUR {item.total:.2f}'
        }
        for item in invoice.items
    ],
    'subtotal': f'EUR {invoice.subtotal:.2f}',
    'vat': f'EUR {invoice.vat_amount:.2f}',
    'total': f'EUR {invoice.total:.2f}',
}

# Genera il PDF
generator = InvoiceGenerator(company_name='KOBAK S.r.l.')
generator.generate(data, f'/path/to/invoices/{invoice.number}.pdf')
```
