"""
Esempio 4: Multi-pagina con Header e Footer
PDF con più pagine e intestazione/piè di pagina automatici
"""
from fpdf import FPDF
from datetime import datetime

class MyPDF(FPDF):
    """Classe personalizzata con header e footer"""
    
    def header(self):
        # Logo o titolo nell'header
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, text='Report Mensile', border=0, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)
    
    def footer(self):
        # Posiziona il footer a 15mm dal fondo
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        
        # Numero di pagina
        self.cell(0, 10, text=f'Pagina {self.page_no()}/{{nb}}', align='C')

def create_multipage_pdf():
    pdf = MyPDF()
    pdf.alias_nb_pages()  # Per il totale pagine
    
    # Aggiungi più pagine
    for i in range(3):
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, text=f'Sezione {i+1}', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        pdf.set_font('Helvetica', '', 11)
        
        # Genera del testo lorem ipsum
        for j in range(20):
            text = f"Questa è la riga {j+1} della sezione {i+1}. " \
                   f"fpdf2 gestisce automaticamente il passaggio alla pagina successiva quando necessario."
            pdf.multi_cell(0, 6, text=text)
        
        pdf.ln(10)
        
        # Data di generazione
        if i == 2:  # Ultima pagina
            pdf.set_font('Helvetica', 'I', 9)
            pdf.cell(0, 10, text=f'Generato il: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 
                    align='R')
    
    pdf.output("../output/04_multi_page.pdf")
    print("✓ PDF creato: output/04_multi_page.pdf")

if __name__ == "__main__":
    create_multipage_pdf()
