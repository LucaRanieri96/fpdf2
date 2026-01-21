from pathlib import Path
import sys
import os

# Aggiungi la directory parent al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.base_pdf import KobakPDF, COLORS
from fpdf.enums import XPos, YPos, Align
from datetime import datetime

class KobakContractPDF(KobakPDF):
    """
    Generatore PDF per contratti Kobak.
    Eredita componenti riutilizzabili da KobakPDF (base_pdf.py).
    """
    
    def __init__(self, orientation='P', format='A4', font='Helvetica'):
        super().__init__(
            font=font,
            company_name="KOBAK S.r.l.",
            orientation=orientation,
            format=format
        )
        
        # Configurazione specifica per contratti
        self.set_margins(left=5, top=15, right=5)
        self.set_auto_page_break(auto=True, margin=20)
        
        # Metadata
        self.set_title("Contratto Kobak")
        self.set_author("KOBAK S.r.l.")
    
    def header(self):
        """Header con logo e info azienda"""
        # Logo (simulato con testo)
        self.set_font(self.font_family, 'B', 14)
        self.set_text_color(*COLORS['primary'])
        self.set_y(10)
        self.cell(0, 8, "KOBAK", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)

        # Info azienda
        self.set_font(self.font_family, '', 7)
        self.set_text_color(*COLORS['text_dark'])
        self.cell(0, 4, "KOBAK FRANCE SARL - 66 Avenue des Champs-Élysées - 75008, Paris - France", 
                 align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.cell(0, 4, "Téléphone: 0184746287 - Mail: info@kobakfrance.fr", 
                 align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)
        
        # Linea separatrice gialla (usando componente base)
        self.draw_horizontal_line(color=COLORS['primary'], width=0.5, y=self.get_y() + 2)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        
        self.ln(5)
    
    def footer(self):
        """Footer con numero pagina"""
        self.set_y(-15)
        self.set_font(self.font_family, 'I', 8)
        self.set_text_color(*COLORS['text_light'])
        
        # Testo footer
        self.cell(0, 5, "SERVIZIO EFFETTUATO IN CONFORMITA' CON LA UNI EN 16194", 
                 align=Align.L, new_x=XPos.RIGHT)
        
        # Numero pagina
        self.cell(0, 5, f"Pagina {self.page_no()}/{{nb}}", align=Align.R)
    
    def add_section_header(self, text, color='primary', width=None):
        """
        Intestazione sezione (usa componente base con mappatura colori legacy).
        Questo metodo mantiene compatibilità con il codice esistente.
        """
        # Mappa i vecchi nomi colori ai nuovi
        color_map = {
            'primary': 'primary',
            'secondary': 'chip_gray'
        }
        
        bg_color = color_map.get(color, 'primary')
        text_color = 'text_dark' if color == 'primary' else 'text_white'
        
        # Chiama il componente base
        from generators.base_pdf import COLORS
        self.set_fill_color(*COLORS[bg_color])
        self.set_text_color(*COLORS[text_color])
        self.set_font(self.font_family, 'B', 9)
        
        cell_width = width if width else 0
        y_pos = self.get_y()
        x_pos = self.get_x()
        rect_width = cell_width if cell_width > 0 else (self.w - self.l_margin - self.r_margin)
        
        self.rounded_rect(x_pos, y_pos, rect_width, 7, 2, style='F')
        
        self.cell(cell_width, 7, text, border=0, align=Align.C, fill=False, 
                 new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.ln(2)
        
        # Reset colors
        self.set_text_color(*COLORS['text_dark'])
        self.set_fill_color(*COLORS['bg_white'])
    
    def add_gray_header(self, text, width=None):
        """Intestazione grigia"""
        self.add_section_header(text, color='secondary', width=width)
    
    def add_two_column_with_headers(self, left_header, left_content_fn, right_header, right_content_fn, col_ratio=0.5):
        """
        Sezione a due colonne con header separati.
        Usa il componente base add_columns_with_headers.
        """
        self.add_columns_with_headers(
            left_header=left_header,
            left_fn=left_content_fn,
            right_header=right_header,
            right_fn=right_content_fn,
            col_ratio=col_ratio,
            gutter=3,
            left_header_bg='primary',
            right_header_bg='chip_gray'
        )
        self.ln(3)
    
    def add_info_line(self, label, value, label_width=None):
        """
        Riga informativa (usa componente base).
        """
        self.add_label_value_line(
            label=label,
            value=value,
            label_width=label_width,
            line_height=4,
            font_size=7
        )
    
    # Metodo rimosso: add_two_column_section (non più usato)
    # Metodo rimosso: add_checkbox_row (ora usa componente base)
    
    def add_services_table(self, services_data):
        """
        Tabella dettagli servizi usando componente base add_zebra_table.
        """
        headers = ['DESCRIZIONE', 'QTÀ', 'UNITÀ', 'PREZZO UNIT. (EUR)', 'TOTALE (EUR)']
        col_widths = [0.40, 0.10, 0.15, 0.17, 0.18]
        aligns = ['L'] + ['C'] * (len(headers) - 1)
        
        self.add_zebra_table(
            headers=headers,
            rows=services_data,
            col_widths=col_widths,
            aligns=aligns,
            header_bg='bg_light',
            zebra_color='bg_light',
            header_font_size=6,
            row_font_size=6.5,
            row_height=7
        )
    
    def add_totals_section(self, totals_data):
        """
        Sezione totali usando componente base add_table_row_with_fill.
        """
        self.ln(2)
        
        for label, value in totals_data:
            self.add_table_row_with_fill(
                cells=[label, value],
                widths=[0.65, 0.35],
                height=5,
                fill=True,
                fill_color=COLORS['bg_light'],
                font_style='B',
                font_size=7,
                aligns=['L', 'R'],
                corner_radius=1
            )
            # Linea separatrice sottile
            self.draw_horizontal_line(color=(200, 200, 200), width=0.1)
        
        self.ln(2)
    
    def add_signature_section(self, left_title, right_title):
        """
        Sezione firme affiancate usando componente base add_columns_with_headers.
        """
        # Salva content_width per calcoli
        col_width = self.content_width * 0.5 - 2
        
        def left_signature():
            # Forza X all'inizio della colonna sinistra
            x_start = self.l_margin
            self.set_x(x_start)
            self.set_font(self.font_family, '', 7)
            self.cell(col_width, 4, "Luogo .................................................................,", new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.set_x(x_start)
            self.cell(col_width, 4, "Data ......./....../..............", new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.ln(5)
            
            self.set_x(x_start)
            self.cell(col_width, 4, "IL CLIENTE", new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.set_x(x_start)
            self.cell(col_width, 4, "(Timbro e Firma)", new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.ln(2)
            
            # Linea firma
            self.set_x(x_start)
            self.cell(col_width, 0.3, "", border='B', new_x=XPos.LEFT, new_y=YPos.NEXT)
        
        def right_signature():
            # Forza X all'inizio della colonna destra
            x_start = self.l_margin + self.content_width * 0.5 + 2
            self.set_x(x_start)
            self.set_font(self.font_family, '', 7)
            self.cell(col_width, 4, "Ritirare i Bagni Dal ......./....../..............", new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.ln(5)
            
            self.set_x(x_start)
            self.cell(col_width, 4, "IL CLIENTE", new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.set_x(x_start)
            self.cell(col_width, 4, "(Timbro e Firma)", new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.ln(2)
            
            # Linea firma
            self.set_x(x_start)
            self.cell(col_width, 0.3, "", border='B', new_x=XPos.LEFT, new_y=YPos.NEXT)
        
        self.add_columns_with_headers(
            left_header=left_title,
            left_fn=left_signature,
            right_header=right_title,
            right_fn=right_signature,
            col_ratio=0.5,
            gutter=4
        )
        
        self.ln(5)
    
    def add_contract_terms(self, terms):
        """Condizioni contrattuali"""
        self.add_section_header("CONDIZIONI CONTRATTUALI")
        self.ln(3)
        
        self.set_font(self.font_family, '', 6.5)
        
        for i, term in enumerate(terms, 1):
            # Numero punto
            self.set_font(self.font_family, 'B', 6.5)
            self.cell(10, 3.5, f"{i}.", new_x=XPos.RIGHT)
            
            # Testo
            self.set_font(self.font_family, '', 6.5)
            self.multi_cell(0, 3.5, term)
            self.ln(1)
    
    def generate_contract(self, contract_data, output_path="contratto_kobak.pdf"):
        """Genera il contratto completo"""
        self.add_page()
        
        # SEZIONE OFFERTA
        self.add_section_header("OFFERTA")
        page_width = self.w - self.l_margin - self.r_margin
        
        self.set_x(self.l_margin)
        self.set_font(self.font_family, 'B', 7)
        self.cell(25, 4, "Offerta n.", new_x=XPos.RIGHT)
        self.set_font(self.font_family, '', 7)
        self.cell(page_width - 25, 4, f"{contract_data['order_number']} - {contract_data['sede']} del {contract_data['rental_start_date']}", new_x=XPos.LEFT, new_y=YPos.NEXT)
        
        self.set_x(self.l_margin)
        self.set_font(self.font_family, 'B', 7)
        self.cell(40, 4, "Validità offerta gg:", new_x=XPos.RIGHT)
        self.set_font(self.font_family, '', 7)
        self.cell(page_width - 40, 4, str(contract_data['rental_days']), new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.ln(3)
        
        # SEZIONE DATI CLIENTE + SEDE DI POSTA (due colonne)
        client = contract_data['client']
        post_office = contract_data['post_office']
        
        # Prepara dati cliente
        client_rows = [
            ('Azienda:', client['company_name']),
            ('Indirizzo:', client['address']),
            ('CAP/Città:', f"{client['postal_code']} {client['city']}"),
            ('Tel.:', client['phone']),
            ('Fax:', client['fax']),
            ('Mail:', client['email']),
            ('PEC:', client['pec']),
            ('Partita IVA:', client['vat_number']),
            ('Codice Fiscale:', client['tax_code']),
            ('IPA/SDI:', client['ipa_sdi'])
        ]
        
        # Prepara dati sede
        post_rows = [
            ('Indirizzo:', post_office['address']),
            ('Indirizzo 2:', post_office['address2']),
            ('Indirizzo 3:', post_office['address3'])
        ]
        
        # Usa componente base per layout a due colonne
        self.add_two_column_info_boxes(
            left_header='DATI DEL CLIENTE',
            left_rows=client_rows,
            right_header='SEDE DI POSTA',
            right_rows=post_rows,
            left_header_bg='primary',
            right_header_bg='chip_gray'
        )
        
        self.ln(3)
        
        # SPEDIZIONE FATTURE
        self.add_gray_header("SPEDIZIONE FATTURE")
        self.set_font(self.font_family, '', 7)
        self.multi_cell(0, 3.5, "Barrare il metodo alternativo scelto per la spedizione delle fatture:")
        self.ln(1)
        
        # Usa componente base per checkbox
        self.add_form_checkboxes([
            "Solo Fattura Elettronica",
            "Anche Posta Cartacea",
            "Anche Mail o PEC al seguente indirizzo:"
        ], spacing=1)
        
        # Linea per indirizzo email
        self.cell(0, 4, "........................................................................", new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.ln(3)
        
        # SEZIONE ESECUTORE SERVIZI
        self.add_section_header("ESECUTORE DEI SERVIZI")
        executor = contract_data['executor']
        
        # Prepara dati esecutore
        executor_rows = [
            ('Azienda:', executor['company_name']),
            ('Indirizzo:', executor['address']),
            ('CAP/Città:', f"{executor['postal_code']} {executor['city']}")
        ]
        
        # Prepara dati contatti
        contact_rows = [
            ('Tel.:', executor['phone']),
            ('Fax:', executor['fax']),
            ('Mail:', executor['email'])
        ]
        
        # Layout a due colonne (60/40)
        def left_fn():
            self.add_info_grid(executor_rows, label_width=25)
        
        def right_fn():
            self.add_info_grid(contact_rows, label_width=15)
        
        self.add_two_columns_with_callbacks(
            left_fn=left_fn,
            right_fn=right_fn,
            col_ratio=0.6,
            gutter=3
        )
        
        self.ln(3)
        
        # SEZIONE SERVIZI OFFERTI
        self.add_section_header("SERVIZI OFFERTI")
        self.add_gray_header("UBICAZIONE BAGNI")
        
        services = contract_data['services']
        self.add_info_grid([
            ('Ubicazione Bagni:', services['location']),
            ('Indirizzo:', services['address']),
            ('Responsabile:', services['manager'])
        ], label_width=38)
        
        self.ln(3)
        
        # SEZIONE DETTAGLI SERVIZI
        self.add_section_header("DETTAGLI SERVIZI")
        self.add_services_table(contract_data['service_items'])
        
        # SEZIONE TOTALI (attaccata alla tabella)
        self.add_totals_section(contract_data['totals'])
        
        # Nuova pagina per pagamento e firme
        self.add_page()
        
        # SEZIONE PAGAMENTO
        self.add_gray_header("PAGAMENTO")
        payment = contract_data['payment']
        self.add_info_grid([('Metodo:', payment['method'])], label_width=38)
        self.ln(5)
        
        # SEZIONE BANCA
        self.add_gray_header("BANCA")
        bank = contract_data['bank']
        self.add_info_grid([
            ('Nome:', bank['name']),
            ('Sede:', bank['branch']),
            ('IBAN:', bank['iban']),
            ('ABI:', bank['abi']),
            ('CAB:', bank['cab'])
        ], label_width=38)
        self.ln(10)
        
        # SEZIONE FIRME
        self.add_signature_section("PER ACCETTAZIONE", "PER DISDETTA")
        
        # SEZIONE CONDIZIONI CONTRATTUALI
        self.add_page()
        self.add_contract_terms(contract_data['contract_terms'])
        
        # FIRMA FINALE
        self.ln(10)
        self.set_font(self.font_family, 'B', 9)
        self.multi_cell(0, 6, "LETTO CONFERMATO E SOTTOSCRITTO")
        self.ln(5)
        
        # Firma cliente
        self.set_font(self.font_family, '', 9)
        self.cell(60, 6, "IL CLIENTE", new_x=XPos.RIGHT)
        self.cell(0, 6, "(Timbro e Firma)", align=Align.R)
        self.ln(10)
        
        # Linea firma
        self.cell(0, 1, "", border='B')
        self.ln(15)
        
        # Approvazione clausole
        self.set_font(self.font_family, '', 7)
        approval_text = """Ai sensi e per gli effetti dell'art. 1341, secondo comma, Cod. Civ. le parti approvano espressamente gli artt. 3. (Obblighi e divieti del cliente), 4. (Conformità), 5. (Durata e rinnovo), 9. (Clausola risolutiva), 10. (Contestazioni), 11. (Limitazioni di responsabilità), 15. (Foro Competente)"""
        self.multi_cell(0, 4, approval_text)
        self.ln(10)
        
        # Seconda firma
        self.set_font(self.font_family, 'B', 9)
        self.multi_cell(0, 6, "LETTO CONFERMATO E SOTTOSCRITTO")
        self.ln(5)
        
        self.set_font(self.font_family, '', 9)
        self.cell(60, 6, "IL CLIENTE", new_x=XPos.RIGHT)
        self.cell(0, 6, "(Timbro e Firma)", align=Align.R)
        self.ln(10)
        
        self.cell(0, 1, "", border='B')
        
        # Salva il PDF
        self.output(output_path)
        return output_path


# ESEMPIO DI UTILIZZO
def create_sample_contract():
    """Crea un contratto di esempio"""
    
    # Dati di esempio
    contract_data = {
        'order_number': 'OFF-2024-001',
        'sede': 'Sede Principale',
        'rental_start_date': '20/01/2024',
        'rental_days': 30,
        
        'client': {
            'company_name': 'Acme Corporation S.p.A.',
            'address': 'Via Roma 123, 10100 Torino',
            'postal_code': '10100',
            'city': 'Torino',
            'phone': '+39 011 1234567',
            'fax': '+39 011 1234568',
            'email': 'info@acme.com',
            'pec': 'acme@pec.it',
            'vat_number': 'IT12345678901',
            'tax_code': '12345678901',
            'ipa_sdi': 'M5UXCR1'
        },
        
        'post_office': {
            'address': 'Via Torino 456, 10100 Torino',
            'address2': 'Palazzo A, Scala B',
            'address3': 'Interno 15'
        },
        
        'executor': {
            'company_name': 'KOBAK Italia S.r.l.',
            'address': 'Via Trentino-Alto Adige 4',
            'postal_code': '53036',
            'city': 'Poggibonsi (SI)',
            'phone': '+39 0577 123456',
            'fax': '+39 0577 123457',
            'email': 'info@kobak.it'
        },
        
        'services': {
            'location': 'Cantiere Edile Centro Città',
            'address': 'Piazza Duomo 1, 10100 Torino',
            'manager': 'Mario Rossi'
        },
        
        'service_items': [
            ['Bagno Chimico Standard KOBAK', '2', 'n°', '150,00', '300,00'],
            ['Servizio Pulizia Base', '4', 'sett.', '50,00', '200,00'],
            ['Installazione Standard', '1', 'serv.', '100,00', '100,00'],
            ['Bagno Chimico Premium con Sistema di Ventilazione Avanzato, Porta Rinforzata in Acciaio, Illuminazione LED Interna, Dispenser Automatico Sapone e Gel Igienizzante, Specchio Panoramico e Sistema Anti-Odore con Filtri a Carboni Attivi', '3', 'n°', '250,00', '750,00'],
            ['Servizio Pulizia Settimanale Completa con Sanificazione Professionale Certificata, Rifornimento Completo di tutti i Materiali Consumabili inclusi Carta Igienica Premium, Sapone Antibatterico, Gel Igienizzante Mani e Deodorante Ambientale', '8', 'sett.', '75,00', '600,00'],
            ['Bagno Chimico per Disabili Conforme Normativa Europea con Accesso Facilitato, Maniglioni di Sicurezza, Spazio Interno Maggiorato e Sistema di Emergenza con Allarme', '1', 'n°', '200,00', '200,00'],
            ['Servizio Manutenzione Straordinaria', '2', 'interv.', '120,00', '240,00'],
            ['Trasporto Speciale Urgente con Mezzo Dedicato e Installazione Express entro 24 ore dalla Richiesta con Personale Specializzato e Certificato per Interventi in Cantieri Edili e Zone a Traffico Limitato', '1', 'serv.', '180,00', '180,00'],
        ],
        
        'totals': [
            ('TOTALE IMPONIBILE', 'EUR 2.570,00'),
            ('FURTI, INCENDI E ATTI VANDALICI (5%)', 'EUR 128,50'),
            ('IVA (22%)', 'EUR 565,40'),
            ('TOTALE COMPLESSIVO', 'EUR 3.263,90')
        ],
        
        'payment': {
            'method': 'Bonifico Bancario 30gg FF'
        },
        
        'bank': {
            'name': 'Banca KOBAK',
            'branch': 'Filiale Centrale',
            'iban': 'IT60X0542811101000000123456',
            'abi': '05428',
            'cab': '11101'
        },
        
        'contract_terms': [
            "(Il Contratto). Il Contratto si compone dell'Offerta e delle Condizioni Contrattuali...",
            "(Oggetto del contratto). Il CLIENTE dichiara di conoscere il funzionamento dei bagni chimici KOBAK...",
            "(Obblighi e divieti del cliente). Il CLIENTE deve pagare il canone di noleggio nei termini indicati...",
        ]
    }
    
    # Crea il PDF
    pdf = KobakContractPDF()
    output_file = pdf.generate_contract(contract_data, "contratto_kobak_esempio.pdf")
    
    return output_file


if __name__ == "__main__":
    # Crea un contratto di esempio
    try:
        output_path = create_sample_contract()
        print(f"✓ Contratto generato con successo: {output_path}")
    except Exception as e:
        print(f"❌ Errore nella generazione del contratto: {e}")