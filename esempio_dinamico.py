"""
ESEMPIO: Come usare i componenti dinamici di base_pdf.py

I componenti accettano LISTE e le compongono automaticamente!
Non serve codice ripetitivo, basta passare i dati.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from generators.base_pdf import KobakPDF

# ==================== ESEMPIO 1: Info Section Singola ====================
def esempio_singola_colonna():
    """Sezione info semplice con header"""
    pdf = KobakPDF()
    pdf.add_page()
    
    # Dati cliente (puoi cambiarli a piacere!)
    cliente = {
        'nome': 'Mario Rossi',
        'azienda': 'Acme Corporation',
        'telefono': '+39 011 123456',
        'email': 'mario@acme.com',
        'partita_iva': 'IT12345678901'
    }
    
    # Converti il dict in lista di tuple
    righe = [
        ('Nome:', cliente['nome']),
        ('Azienda:', cliente['azienda']),
        ('Telefono:', cliente['telefono']),
        ('Email:', cliente['email']),
        ('P.IVA:', cliente['partita_iva'])
    ]
    
    # UN SOLO METODO, passa la lista e lui fa tutto!
    pdf.add_info_section(
        header='DATI CLIENTE',
        rows=righe,
        header_bg='primary'
    )
    
    pdf.output('esempio_singola.pdf')
    print("✓ PDF singola colonna creato!")


# ==================== ESEMPIO 2: Due Colonne ====================
def esempio_due_colonne():
    """Due sezioni affiancate con header diversi"""
    pdf = KobakPDF()
    pdf.add_page()
    
    # Dati cliente (source può essere DB, API, form...)
    cliente_data = {
        'azienda': 'Acme Corporation S.p.A.',
        'indirizzo': 'Via Roma 123, 10100 Torino',
        'telefono': '+39 011 1234567',
        'email': 'info@acme.com',
        'piva': 'IT12345678901'
    }
    
    # Dati sede (altra fonte dati)
    sede_data = {
        'via': 'Via Milano 456',
        'civico': 'Palazzo A, Scala 2',
        'citta': '10100 Torino',
        'note': 'Citofono "Acme"'
    }
    
    # Converti in liste
    righe_cliente = [
        ('Azienda:', cliente_data['azienda']),
        ('Indirizzo:', cliente_data['indirizzo']),
        ('Tel.:', cliente_data['telefono']),
        ('Email:', cliente_data['email']),
        ('P.IVA:', cliente_data['piva'])
    ]
    
    righe_sede = [
        ('Via:', sede_data['via']),
        ('Civico:', sede_data['civico']),
        ('Città:', sede_data['citta']),
        ('Note:', sede_data['note'])
    ]
    
    # UN SOLO METODO per entrambe le colonne!
    pdf.add_info_section(
        two_columns=True,
        left_header='DATI CLIENTE',
        left_rows=righe_cliente,
        left_header_bg='primary',
        right_header='SEDE DI CONSEGNA',
        right_rows=righe_sede,
        right_header_bg='chip_gray'
    )
    
    pdf.output('esempio_due_colonne.pdf')
    print("✓ PDF due colonne creato!")


# ==================== ESEMPIO 3: Tabella Dinamica ====================
def esempio_tabella():
    """Tabella con dati variabili"""
    pdf = KobakPDF()
    pdf.add_page()
    
    # Dati servizi (potrebbero venire da DB)
    servizi = [
        {'nome': 'Bagno Chimico Standard', 'qty': 2, 'prezzo': 150.00},
        {'nome': 'Pulizia Settimanale', 'qty': 4, 'prezzo': 50.00},
        {'nome': 'Installazione', 'qty': 1, 'prezzo': 100.00},
        {'nome': 'Manutenzione Straordinaria', 'qty': 2, 'prezzo': 120.00}
    ]
    
    # Converti in formato per zebra_table
    headers = ['Descrizione', 'Quantità', 'Prezzo Unitario', 'Totale']
    righe = [
        [
            s['nome'], 
            str(s['qty']), 
            f"EUR {s['prezzo']:.2f}", 
            f"EUR {s['qty'] * s['prezzo']:.2f}"
        ]
        for s in servizi
    ]
    
    # UN SOLO METODO, gestisce tutto automaticamente!
    pdf.add_zebra_table(
        headers=headers,
        rows=righe,
        col_widths=[0.5, 0.15, 0.15, 0.20],  # Frazioni di larghezza
        aligns=['L', 'C', 'R', 'R']
    )
    
    pdf.output('esempio_tabella.pdf')
    print("✓ PDF tabella creato!")


# ==================== ESEMPIO 4: Da Dict/JSON ====================
def esempio_da_json():
    """Esempio realistico: dati da API/Database"""
    import json
    
    # Simula risposta API o query database
    dati_api = {
        "cliente": {
            "ragione_sociale": "Tech Solutions Ltd",
            "referente": "Giovanni Bianchi",
            "contatti": {
                "telefono": "+39 02 9876543",
                "mobile": "+39 333 1234567",
                "email": "g.bianchi@techsol.com",
                "pec": "techsol@pec.it"
            },
            "fiscali": {
                "partita_iva": "IT98765432109",
                "codice_fiscale": "BNCGNN80A01F205X",
                "codice_sdi": "XXXXXX"
            }
        },
        "progetto": {
            "codice": "PROJ-2024-042",
            "descrizione": "Fornitura bagni chimici cantiere",
            "data_inizio": "01/02/2024",
            "data_fine": "31/03/2024",
            "responsabile": "Arch. Maria Verdi"
        }
    }
    
    pdf = KobakPDF()
    pdf.add_page()
    
    # Estrai e converti automaticamente
    cliente = dati_api['cliente']
    righe_cliente = [
        ('Ragione Sociale:', cliente['ragione_sociale']),
        ('Referente:', cliente['referente']),
        ('Telefono:', cliente['contatti']['telefono']),
        ('Mobile:', cliente['contatti']['mobile']),
        ('Email:', cliente['contatti']['email']),
        ('PEC:', cliente['contatti']['pec']),
        ('Partita IVA:', cliente['fiscali']['partita_iva']),
        ('Codice Fiscale:', cliente['fiscali']['codice_fiscale']),
        ('Codice SDI:', cliente['fiscali']['codice_sdi'])
    ]
    
    progetto = dati_api['progetto']
    righe_progetto = [
        ('Codice Progetto:', progetto['codice']),
        ('Descrizione:', progetto['descrizione']),
        ('Data Inizio:', progetto['data_inizio']),
        ('Data Fine:', progetto['data_fine']),
        ('Responsabile:', progetto['responsabile'])
    ]
    
    # Layout completo con un colpo solo
    pdf.add_info_section(
        two_columns=True,
        left_header='CLIENTE',
        left_rows=righe_cliente,
        left_header_bg='primary',
        right_header='PROGETTO',
        right_rows=righe_progetto,
        right_header_bg='chip_gray',
        col_ratio=0.6  # Cliente più largo
    )
    
    pdf.output('esempio_da_api.pdf')
    print("✓ PDF da dati API/DB creato!")


# ==================== ESEMPIO 5: Multipli Tipi ====================
def esempio_completo():
    """PDF completo con diverse sezioni"""
    pdf = KobakPDF()
    pdf.add_page()
    
    # TITOLO
    pdf.add_document_title("PREVENTIVO N. 2024/042")
    pdf.ln(5)
    
    # INFO DOCUMENTO (singola colonna senza header)
    pdf.add_info_section(rows=[
        ('Data Emissione:', '21/01/2024'),
        ('Validità:', '30 giorni')
    ])
    pdf.ln(5)
    
    # CLIENTE + SEDE (due colonne)
    pdf.add_info_section(
        two_columns=True,
        left_header='CLIENTE',
        left_rows=[
            ('Nome:', 'Costruzioni Moderne SpA'),
            ('P.IVA:', 'IT11223344556'),
            ('Tel.:', '+39 011 556677')
        ],
        right_header='CANTIERE',
        right_rows=[
            ('Indirizzo:', 'Via Cantiere 100'),
            ('Città:', 'Milano'),
            ('Referente:', 'Ing. Rossi')
        ]
    )
    pdf.ln(5)
    
    # TABELLA SERVIZI
    pdf.add_section_heading("Servizi Richiesti")
    pdf.add_zebra_table(
        headers=['Descrizione', 'Quantità', 'Prezzo'],
        rows=[
            ['Bagno Chimico Standard', '5', 'EUR 150,00'],
            ['Pulizia Settimanale', '8', 'EUR 50,00'],
            ['Installazione', '1', 'EUR 100,00']
        ],
        col_widths=[0.6, 0.2, 0.2],
        aligns=['L', 'C', 'R']
    )
    pdf.ln(5)
    
    # TOTALI (singola colonna con header)
    pdf.add_info_section(
        header='TOTALI',
        header_bg='chip_gray',
        rows=[
            ('Imponibile:', 'EUR 1.150,00'),
            ('IVA 22%:', 'EUR 253,00'),
            ('TOTALE:', 'EUR 1.403,00')
        ],
        label_width=40
    )
    
    pdf.output('esempio_completo.pdf')
    print("✓ PDF completo creato!")


if __name__ == '__main__':
    print("🚀 Generazione esempi PDF dinamici...\n")
    
    esempio_singola_colonna()
    esempio_due_colonne()
    esempio_tabella()
    esempio_da_json()
    esempio_completo()
    
    print("\n✅ Tutti i PDF sono stati generati!")
    print("\n💡 Vedi come basta passare LISTE e il componente fa tutto?")
    print("   - Niente codice ripetitivo")
    print("   - Dati da qualsiasi fonte (DB, API, form...)")
    print("   - Layout automatico responsive")
