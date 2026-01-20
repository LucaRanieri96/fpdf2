"""
Esempio 2: Formattazione Base
Testo con diversi stili, dimensioni e colori
"""
from fpdf import FPDF

def create_formatted_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Titolo grande e bold
    pdf.set_font('Helvetica', 'B', 24)
    pdf.cell(200, 10, text="Formattazione Testo", new_x="LMARGIN", new_y="NEXT", align='C')
    
    # Spazio vuoto
    pdf.ln(10)
    
    # Testo normale
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(200, 10, text="Questo è testo normale", new_x="LMARGIN", new_y="NEXT")
    
    # Testo in grassetto
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(200, 10, text="Questo è testo in grassetto", new_x="LMARGIN", new_y="NEXT")
    
    # Testo in corsivo
    pdf.set_font('Helvetica', 'I', 12)
    pdf.cell(200, 10, text="Questo è testo in corsivo", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(5)
    
    # Testo con colore
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(255, 0, 0)  # Rosso
    pdf.cell(200, 10, text="Testo rosso", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_text_color(0, 128, 0)  # Verde
    pdf.cell(200, 10, text="Testo verde", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_text_color(0, 0, 255)  # Blu
    pdf.cell(200, 10, text="Testo blu", new_x="LMARGIN", new_y="NEXT")
    
    # Ritorna a nero
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(10)
    
    # Multi-cell per testo lungo
    pdf.set_font('Helvetica', '', 10)
    long_text = "Questo è un testo più lungo che viene automaticamente diviso su più righe " \
                "quando necessario. fpdf2 gestisce automaticamente il line breaking!"
    pdf.multi_cell(0, 5, text=long_text)
    
    pdf.output("../output/02_basic_formatting.pdf")
    print("✓ PDF creato: output/02_basic_formatting.pdf")

if __name__ == "__main__":
    create_formatted_pdf()
