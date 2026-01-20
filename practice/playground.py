import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.base_pdf import KobakPDF, COLORS


OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def showcase_components():
    pdf = KobakPDF(
        company_name="KOBAK S.r.l.",
        company_info=[
            "Sede: Via Roma 10, 10100 Torino",
            "Tel: +39 011 1234567 - Mail: info@kobak.it",
        ],
    )
    pdf.alias_nb_pages()

    gallery = [
        ("Document Title", render_document_title),
        ("Document + Client Info", render_document_and_client_info),
        ("Items Table", render_items_table),
        ("Totals Section", render_totals_box),
        ("Notes Section", render_notes_box),
        ("Validity Info", render_validity_card),
        ("Section Heading", render_section_heading),
        ("Section Chip", render_section_chip),
        ("Info Card", render_info_card),
        ("Details Table", render_details_table),
        ("Totals List", render_totals_list),
        ("Signature Blocks", render_signature_blocks),
        ("Contract Terms", render_contract_terms),
    ]

    for title, renderer in gallery:
        pdf.add_page()
        add_component_header(pdf, title)
        renderer(pdf)

    output_path = OUTPUT_DIR / "components_gallery.pdf"
    pdf.output(str(output_path))
    print(f"✓ PDF creato: {output_path.relative_to(Path.cwd())}")


def add_component_header(pdf: KobakPDF, name: str):
    pdf.set_font(pdf.font_family, 'B', 14)
    pdf.set_text_color(*COLORS['secondary_dark'])
    pdf.cell(0, 8, text=f"Component: {name}")
    pdf.ln(6)


def render_document_title(pdf: KobakPDF):
    pdf.add_document_title('FATTURA COMMERCIALE')


def render_document_and_client_info(pdf: KobakPDF):
    info_y, info_h, col_width, gutter = pdf.add_document_info(
        number='FAT-2026-001',
        date='20/01/2026',
        label_prefix='Fattura'
    )
    pdf.add_client_info(
        client_name='Acme Corporation',
        vat_number='IT12345678901',
        address='Via Milano 12, 10100 Torino',
        anchor_y=info_y,
        col_width=col_width,
        gutter=gutter
    )
    pdf.set_y(info_y + info_h + 5)


def render_items_table(pdf: KobakPDF):
    items = [
        {'description': 'Noleggio bagni chimici standard', 'qty': 10, 'unit_price': 'EUR 150,00', 'total': 'EUR 1.500,00'},
        {'description': 'Pulizia straordinaria', 'qty': 4, 'unit_price': 'EUR 200,00', 'total': 'EUR 800,00'},
        {'description': 'Trasporto mezzi speciali', 'qty': 1, 'unit_price': 'EUR 450,00', 'total': 'EUR 450,00'},
    ]
    pdf.add_items_table(items)


def render_totals_box(pdf: KobakPDF):
    pdf.add_totals_section(
        subtotal='EUR 2.750,00',
        vat='EUR 605,00',
        total='EUR 3.355,00',
        vat_rate='22%'
    )


def render_notes_box(pdf: KobakPDF):
    pdf.add_notes_section('Pagamento a 30 giorni data fattura. In caso di ritardi si applicano interessi di mora del 2%.')


def render_validity_card(pdf: KobakPDF):
    pdf.add_validity_info('20/02/2026')


def render_section_heading(pdf: KobakPDF):
    pdf.add_section_heading('Intestazione Sezione di Prova')
    pdf.add_paragraph('Testo di esempio per mostrare la distanza e la linea separatrice associate al componente.')


def render_section_chip(pdf: KobakPDF):
    pdf.add_section_chip('Offerta', variant='gold')
    pdf.add_section_chip('Tracciabilita', variant='gray')


def render_info_card(pdf: KobakPDF):
    rows = [
        ('Azienda', 'KOBAK France SARL'),
        ('Indirizzo', '66 Avenue des Champs-Elysees, Paris'),
        ('Tel.', '+33 1 84 74 62 87'),
        ('Mail', 'info@kobak.fr'),
    ]
    pdf.add_info_card('Dati Cliente', rows)


def render_details_table(pdf: KobakPDF):
    rows = [
        {
            'description': 'Servizio completo di noleggio con manutenzione',
            'quantity': 12,
            'unit': 'pz',
            'unit_price': 'EUR 140,00',
            'total_price': 'EUR 1.680,00',
        },
        {
            'description': 'Pulizia extra su richiesta',
            'quantity': 6,
            'unit': 'interventi',
            'unit_price': 'EUR 90,00',
            'total_price': 'EUR 540,00',
        },
    ]
    pdf.add_details_table(rows)


def render_totals_list(pdf: KobakPDF):
    totals = [
        ('TOTALE IMPONIBILE', 'EUR 2.220,00'),
        ('FURTI INCENDI (5%)', 'EUR 111,00'),
        ('IVA (22%)', 'EUR 513,42'),
        ('TOTALE COMPLESSIVO', 'EUR 2.844,42'),
    ]
    pdf.add_totals_list(totals)


def render_signature_blocks(pdf: KobakPDF):
    blocks = [
        {
            'title': 'Per Accettazione',
            'instructions': 'Luogo ...................... Data ......./....../..............',
        },
        {
            'title': 'Per Disdetta',
            'instructions': 'Ritirare i bagni dal ......./....../..............',
        },
    ]
    pdf.add_signature_blocks(blocks)


def render_contract_terms(pdf: KobakPDF):
    clauses = [
        'Il cliente dichiara di conoscere il funzionamento dei bagni e li ritiene idonei.',
        "Il cliente deve garantire l'accesso ai mezzi Kobak e non spostare i bagni senza autorizzazione.",
        'Kobak puo sospendere i servizi in caso di mancato pagamento nei termini.',
    ]
    pdf.add_contract_terms(clauses)


if __name__ == "__main__":
    showcase_components()
