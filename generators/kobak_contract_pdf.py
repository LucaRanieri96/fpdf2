from pathlib import Path
from fpdf import FPDF
from fpdf.enums import XPos, YPos, Align
from datetime import datetime
import os

class KobakContractPDF(FPDF):
    """
    Classe per generare contratti Kobak usando fpdf2
    Basato sul template HTML originale
    """
    
    def __init__(self, orientation='P', format='A4', font='Helvetica'):
        super().__init__(orientation=orientation, unit='mm', format=format)
        self.font_family = font
        
        # Configurazione margini e interruzioni pagina
        self.set_margins(left=15, top=15, right=15)
        self.set_auto_page_break(auto=True, margin=20)
        
        # Metadata
        self.set_title("Contratto Kobak")
        self.set_author("KOBAK S.r.l.")
        
        # Colori Kobak
        self.colors = {
            'primary': (255, 215, 0),      # Giallo
            'secondary': (119, 119, 119),  # Grigio
            'bg_light': (246, 246, 246),   # Background chiaro
            'text_dark': (37, 36, 32),     # Testo scuro
            'text_light': (180, 180, 176), # Testo chiaro
            'white': (255, 255, 255),      # Bianco
        }
    
    def header(self):
        """Header con logo e info azienda"""
        # Background header
        self.set_fill_color(*self.colors['bg_light'])
        self.rect(0, 0, self.w, 30, style='F')
        
        # Logo (simulato con testo)
        self.set_font(self.font_family, 'B', 16)
        self.set_text_color(*self.colors['primary'])
        self.cell(0, 10, "KOBAK", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)
        
        # Info azienda
        self.set_font(self.font_family, '', 8)
        self.set_text_color(*self.colors['text_dark'])
        self.cell(0, 5, "KOBAK FRANCE SARL - 66 Avenue des Champs-Élysées - 75008, Paris - France", 
                 align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.cell(0, 5, "Téléphone: 0184746287 - Mail: info@kobakfrance.fr", 
                 align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)
        
        # Linea separatrice
        self.set_draw_color(*self.colors['primary'])
        self.set_line_width(1)
        self.line(self.l_margin, 30, self.w - self.r_margin, 30)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        
        self.ln(10)
    
    def footer(self):
        """Footer con numero pagina"""
        self.set_y(-15)
        self.set_font(self.font_family, 'I', 8)
        self.set_text_color(*self.colors['text_light'])
        
        # Testo footer
        self.cell(0, 5, "SERVIZIO EFFETTUATO IN CONFORMITA' CON LA UNI EN 16194", 
                 align=Align.L, new_x=XPos.RIGHT)
        
        # Numero pagina
        self.cell(0, 5, f"Pagina {self.page_no()}/{{nb}}", align=Align.R)
    
    def add_section_header(self, text, color='primary'):
        """Intestazione sezione colorata"""
        if color == 'primary':
            self.set_fill_color(*self.colors['primary'])
            self.set_text_color(*self.colors['text_dark'])
        else:
            self.set_fill_color(*self.colors['secondary'])
            self.set_text_color(*self.colors['white'])
        
        self.set_font(self.font_family, 'B', 10)
        self.cell(0, 8, text, border=1, align=Align.C, fill=True, 
                 new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.ln(2)
        
        # Reset colors
        self.set_text_color(*self.colors['text_dark'])
        self.set_fill_color(*self.colors['white'])
    
    def add_gray_header(self, text):
        """Intestazione grigia"""
        self.add_section_header(text, color='secondary')
    
    def add_info_line(self, label, value, width=80):
        """Riga informativa (label: value)"""
        self.set_font(self.font_family, 'B', 9)
        self.cell(width, 6, label, new_x=XPos.RIGHT)
        
        self.set_font(self.font_family, '', 9)
        self.cell(0, 6, value, new_x=XPos.LEFT, new_y=YPos.NEXT)
    
    def add_two_column_section(self, left_content, right_content):
        """Sezione a due colonne"""
        # Salva posizione
        x_start = self.get_x()
        y_start = self.get_y()
        
        # Colonna sinistra
        self.multi_cell(self.w / 2 - 10, 6, left_content)
        
        # Ritorna a destra
        self.set_xy(x_start + self.w / 2, y_start)
        
        # Colonna destra
        self.multi_cell(0, 6, right_content)
        
        # Nuova linea
        self.set_x(x_start)
        self.ln(5)
    
    def add_checkbox_row(self, labels):
        """Riga con checkbox"""
        checkbox_size = 4
        for i, label in enumerate(labels):
            # Checkbox
            self.set_draw_color(0, 0, 0)
            self.rect(self.get_x(), self.get_y(), checkbox_size, checkbox_size, style='D')
            self.cell(checkbox_size + 2, checkbox_size, "", new_x=XPos.RIGHT)
            
            # Label
            self.set_font(self.font_family, '', 7)
            self.cell(0, checkbox_size, label, new_x=XPos.RIGHT if i < len(labels) - 1 else XPos.LEFT)
            
            if i < len(labels) - 1:
                self.cell(10, checkbox_size, "", new_x=XPos.RIGHT)
        
        self.ln(6)
    
    def add_services_table(self, services_data):
        """Tabella dettagli servizi"""
        # Intestazione tabella
        self.set_fill_color(*self.colors['bg_light'])
        self.set_font(self.font_family, 'B', 9)
        
        headers = ['DESCRIZIONE', 'QUANTITÀ', 'UNITÀ DI MISURA', 'PREZZO UNITARIO (EUR)', 'PREZZO TOTALE (EUR)']
        col_widths = [60, 20, 25, 30, 30]
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, align=Align.C, fill=True, 
                     new_x=XPos.RIGHT if i < len(headers) - 1 else XPos.LEFT)
        
        self.ln(8)
        
        # Dati servizi
        self.set_font(self.font_family, '', 9)
        self.set_fill_color(*self.colors['white'])
        
        for service in services_data:
            for i, value in enumerate(service):
                align = Align.L if i == 0 else Align.C
                self.cell(col_widths[i], 6, str(value), border=1, align=align, 
                         new_x=XPos.RIGHT if i < len(headers) - 1 else XPos.LEFT)
            self.ln(6)
    
    def add_totals_section(self, totals_data):
        """Sezione totali"""
        self.set_fill_color(232, 232, 232)  # Grigio chiaro
        
        for label, value in totals_data:
            self.set_font(self.font_family, 'B', 9)
            self.cell(0, 6, label, border='B', align=Align.L, fill=True, new_x=XPos.RIGHT)
            
            self.set_font(self.font_family, 'B', 9)
            self.cell(30, 6, value, border='B', align=Align.R, fill=True, 
                     new_x=XPos.LEFT, new_y=YPos.NEXT)
    
    def add_signature_section(self, left_title, right_title):
        """Sezione firme"""
        # Titoli
        self.add_section_header(left_title)
        self.set_x(self.w / 2)
        self.add_section_header(right_title)
        
        self.ln(10)
        
        # Campi firma sinistra
        self.multi_cell(self.w / 2 - 10, 6, "Luogo .................................,")
        self.ln(2)
        self.multi_cell(self.w / 2 - 10, 6, "Data ......./....../..............")
        self.ln(10)
        
        # Firma sinistra
        self.set_font(self.font_family, '', 9)
        self.cell(self.w / 2 - 10, 6, "IL CLIENTE", new_x=XPos.RIGHT)
        self.cell(0, 6, "(Timbro e Firma)", align=Align.R)
        self.ln(10)
        
        # Linea firma
        self.set_x(self.w / 2 - 10)
        self.cell(0, 1, "", border='B', new_x=XPos.LEFT, new_y=YPos.NEXT)
        
        # Campi firma destra
        self.set_x(self.w / 2)
        self.multi_cell(0, 6, "Ritirare i Bagni Dal ......./....../..............")
        self.ln(10)
        
        # Firma destra
        self.set_x(self.w / 2)
        self.set_font(self.font_family, '', 9)
        self.cell(self.w / 2 - 10, 6, "IL CLIENTE", new_x=XPos.RIGHT)
        self.cell(0, 6, "(Timbro e Firma)", align=Align.R)
        self.ln(15)
    
    def add_contract_terms(self, terms):
        """Condizioni contrattuali"""
        self.add_section_header("CONDIZIONI CONTRATTUALI")
        self.ln(5)
        
        self.set_font(self.font_family, '', 7)
        
        for i, term in enumerate(terms, 1):
            # Numero punto
            self.set_font(self.font_family, 'B', 7)
            self.cell(10, 4, f"{i}.", new_x=XPos.RIGHT)
            
            # Testo
            self.set_font(self.font_family, '', 7)
            self.multi_cell(0, 4, term)
            self.ln(2)
    
    def generate_contract(self, contract_data, output_path="contratto_kobak.pdf"):
        """Genera il contratto completo"""
        self.add_page()
        
        # SEZIONE OFFERTA
        self.add_section_header("OFFERTA")
        self.add_info_line("Offerta n.", f"{contract_data['order_number']} - {contract_data['sede']} del {contract_data['rental_start_date']}")
        self.add_info_line("Validità offerta gg:", str(contract_data['rental_days']))
        self.ln(5)
        
        # SEZIONE DATI CLIENTE
        self.add_section_header("DATI DEL CLIENTE")
        client = contract_data['client']
        client_info = f"""Azienda: {client['company_name']}
Indirizzo: {client['address']}
CAP/Città: {client['postal_code']} {client['city']}
Tel.: {client['phone']}
Fax: {client['fax']}
Mail: {client['email']}
PEC: {client['pec']}
Partita IVA: {client['vat_number']}
Codice Fiscale: {client['tax_code']}
IPA/SDI: {client['ipa_sdi']}"""
        
        # SEZIONE SEDE DI POSTA
        post_office_info = f"""Indirizzo: {contract_data['post_office']['address']}
Indirizzo 2: {contract_data['post_office']['address2']}
Indirizzo 3: {contract_data['post_office']['address3']}"""
        
        self.add_two_column_section(client_info, post_office_info)
        
        # SEZIONE SPEDIZIONE FATTURE
        self.add_gray_header("SPEDIZIONE FATTURE")
        self.set_font(self.font_family, '', 9)
        self.multi_cell(0, 6, "Barrare il metodo alternativo scelto per la spedizione delle fatture:")
        self.ln(2)
        
        self.add_checkbox_row(["Solo Fattura Elettronica", "Anche Posta Cartacea"])
        self.add_checkbox_row(["Anche Mail o PEC al seguente indirizzo:"])
        self.multi_cell(0, 6, "................................................................................................")
        self.ln(10)
        
        # SEZIONE ESECUTORE SERVIZI
        self.add_section_header("ESECUTORE DEI SERVIZI")
        executor = contract_data['executor']
        executor_info = f"""Azienda: {executor['company_name']}
Indirizzo: {executor['address']}
CAP/Città: {executor['postal_code']} {executor['city']}"""
        
        executor_contact = f"""Tel.: {executor['phone']}
Fax: {executor['fax']}
Mail: {executor['email']}"""
        
        self.add_two_column_section(executor_info, executor_contact)
        
        # SEZIONE SERVIZI OFFERTI
        self.add_section_header("SERVIZI OFFERTI")
        self.add_gray_header("UBICAZIONE BAGNI")
        
        services = contract_data['services']
        self.add_info_line("Ubicazione Bagni:", services['location'])
        self.add_info_line("Indirizzo:", services['address'])
        self.add_info_line("Responsabile:", services['manager'])
        self.ln(5)
        
        # SEZIONE DETTAGLI SERVIZI
        self.add_section_header("DETTAGLI SERVIZI")
        self.add_services_table(contract_data['service_items'])
        self.ln(5)
        
        # SEZIONE TOTALI
        self.add_totals_section(contract_data['totals'])
        
        # Nuova pagina per pagamento e firme
        self.add_page()
        
        # SEZIONE PAGAMENTO
        self.add_gray_header("PAGAMENTO")
        payment = contract_data['payment']
        self.add_info_line("Metodo:", payment['method'])
        self.ln(5)
        
        # SEZIONE BANCA
        self.add_gray_header("BANCA")
        bank = contract_data['bank']
        self.add_info_line("Nome:", bank['name'])
        self.add_info_line("Sede:", bank['branch'])
        self.add_info_line("IBAN:", bank['iban'])
        self.add_info_line("ABI:", bank['abi'])
        self.add_info_line("CAB:", bank['cab'])
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
            ['Servizio Pulizia Settimanale', '4', 'sett.', '50,00', '200,00'],
            ['Installazione e Ritiro', '1', 'serv.', '100,00', '100,00']
        ],
        
        'totals': [
            ('TOTALE IMPONIBILE', 'EUR 600,00'),
            ('FURTI, INCENDI E ATTI VANDALICI (5%)', 'EUR 30,00'),
            ('IVA (22%)', 'EUR 132,00'),
            ('TOTALE COMPLESSIVO', 'EUR 762,00')
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