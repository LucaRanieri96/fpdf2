"""
Esempio Completo: Fattura/Invoice
Un esempio più realistico che combina vari elementi
"""
from fpdf import FPDF
from datetime import datetime

class InvoicePDF(FPDF):
    def header(self):
        # Logo area (simulato con un box colorato)
        self.set_fill_color(41, 128, 185)
        self.rect(10, 10, 30, 20, 'F')
        
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.set_xy(10, 15)
        self.cell(30, 10, 'LOGO', align='C')
        
        # Reset colori
        self.set_text_color(0, 0, 0)
        
        # Titolo documento
        self.set_xy(50, 10)
        self.set_font('Helvetica', 'B', 24)
        self.cell(0, 10, 'FATTURA', align='R')
        
        self.ln(15)
    
    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        
        # Linea separatrice
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y() - 2, 200, self.get_y() - 2)
        
        # Testo footer
        self.multi_cell(0, 4, 
            'La Mia Azienda S.r.l. | Via Roma 123, 00100 Roma | '
            'P.IVA: 12345678901 | info@miaazienda.it | www.miaazienda.it',
            align='C')

def create_invoice():
    pdf = InvoicePDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Info azienda e cliente - due colonne
    y_start = pdf.get_y()
    
    # Colonna sinistra - Mittente
    pdf.set_xy(10, y_start)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 5, 'DA:', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('Helvetica', '', 9)
    mittente = [
        'La Mia Azienda S.r.l.',
        'Via Roma 123',
        '00100 Roma (RM)',
        'P.IVA: 12345678901',
        'Tel: +39 06 12345678'
    ]
    for line in mittente:
        pdf.cell(0, 4, line, new_x="LMARGIN", new_y="NEXT")
    
    # Colonna destra - Destinatario
    pdf.set_xy(110, y_start)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 5, 'A:', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('Helvetica', '', 9)
    destinatario = [
        'Cliente S.p.A.',
        'Via Milano 456',
        '20100 Milano (MI)',
        'P.IVA: 98765432109',
        'Tel: +39 02 98765432'
    ]
    for line in destinatario:
        pdf.set_x(110)
        pdf.cell(0, 4, line, new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(5)
    
    # Info fattura
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Helvetica', 'B', 10)
    
    info_y = pdf.get_y()
    pdf.set_xy(10, info_y)
    pdf.cell(45, 7, 'Numero Fattura:', border=1, fill=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(45, 7, 'FT-2026-001', border=1)
    
    pdf.set_xy(110, info_y)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(45, 7, 'Data:', border=1, fill=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(45, 7, datetime.now().strftime('%d/%m/%Y'), border=1)
    
    pdf.ln(15)
    
    # Tabella prodotti/servizi
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(52, 152, 219)
    pdf.set_text_color(255, 255, 255)
    
    # Intestazioni
    pdf.cell(90, 10, 'Descrizione', border=1, align='L', fill=True)
    pdf.cell(25, 10, 'Q.tà', border=1, align='C', fill=True)
    pdf.cell(35, 10, 'Prezzo Unit.', border=1, align='C', fill=True)
    pdf.cell(40, 10, 'Totale', border=1, align='C', fill=True, new_x="LMARGIN", new_y="NEXT")
    
    # Reset colori per righe
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 10)
    
    # Dati
    items = [
        ('Consulenza Sviluppo Software', 40, 75.00),
        ('Manutenzione Sistema', 10, 50.00),
        ('Licenza Software (annuale)', 1, 1200.00),
        ('Supporto Tecnico', 20, 60.00),
    ]
    
    subtotal = 0
    alternate = False
    
    for desc, qty, price in items:
        total = qty * price
        subtotal += total
        
        # Alternare colore righe
        if alternate:
            pdf.set_fill_color(250, 250, 250)
            pdf.cell(90, 8, desc, border=1, fill=True)
            pdf.cell(25, 8, str(qty), border=1, align='C', fill=True)
            pdf.cell(35, 8, f'EUR {price:.2f}', border=1, align='R', fill=True)
            pdf.cell(40, 8, f'EUR {total:.2f}', border=1, align='R', fill=True, new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.cell(90, 8, desc, border=1)
            pdf.cell(25, 8, str(qty), border=1, align='C')
            pdf.cell(35, 8, f'EUR {price:.2f}', border=1, align='R')
            pdf.cell(40, 8, f'EUR {total:.2f}', border=1, align='R', new_x="LMARGIN", new_y="NEXT")
        
        alternate = not alternate
    
    pdf.ln(2)
    
    # Totali
    pdf.set_font('Helvetica', 'B', 10)
    
    # Imponibile
    pdf.cell(150, 8, 'Imponibile:', align='R')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(40, 8, f'EUR {subtotal:.2f}', align='R', new_x="LMARGIN", new_y="NEXT")
    
    # IVA
    iva_rate = 0.22
    iva = subtotal * iva_rate
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(150, 8, 'IVA (22%):', align='R')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(40, 8, f'EUR {iva:.2f}', align='R', new_x="LMARGIN", new_y="NEXT")
    
    # Totale
    total = subtotal + iva
    pdf.set_fill_color(52, 152, 219)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(150, 10, 'TOTALE:', fill=True, align='R')
    pdf.cell(40, 10, f'EUR {total:.2f}', fill=True, align='R')
    
    # Reset colori
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(15)
    
    # Note
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'Note:', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(0, 5, 
        'Pagamento entro 30 giorni data fattura.\n'
        'Bonifico bancario: IBAN IT00 X000 0000 0000 0000 0000 000\n'
        'Causale: Fattura FT-2026-001')
    
    pdf.output('../output/06_invoice_example.pdf')
    print('✓ PDF creato: output/06_invoice_example.pdf')

if __name__ == '__main__':
    create_invoice()
