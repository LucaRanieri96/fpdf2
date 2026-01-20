"""
Esempio 1: Hello World
Il primo PDF - semplicissimo!
"""
from fpdf import FPDF

def create_hello_world():
    # Crea un oggetto PDF
    pdf = FPDF()
    
    # Aggiungi una pagina
    pdf.add_page()
    
    # Imposta font (famiglia, stile, dimensione)
    pdf.set_font('Helvetica', size=12)
    
    # Aggiungi testo
    pdf.cell(text="Hello World!")
    
    # Salva il PDF
    pdf.output("../output/01_hello_world.pdf")
    print("✓ PDF creato: output/01_hello_world.pdf")

if __name__ == "__main__":
    create_hello_world()
