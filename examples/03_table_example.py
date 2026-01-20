"""
Esempio 3: Tabelle
Come creare tabelle semplici
"""
from fpdf import FPDF

def create_table_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Titolo
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(200, 10, text="Tabella Prodotti", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)
    
    # Intestazioni tabella
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_fill_color(200, 220, 255)  # Azzurro chiaro
    
    pdf.cell(60, 10, text="Prodotto", border=1, fill=True)
    pdf.cell(40, 10, text="Quantità", border=1, align='C', fill=True)
    pdf.cell(40, 10, text="Prezzo", border=1, align='C', fill=True)
    pdf.cell(40, 10, text="Totale", border=1, new_x="LMARGIN", new_y="NEXT", align='C', fill=True)
    
    # Dati tabella
    pdf.set_font('Helvetica', '', 11)
    
    products = [
        ("Laptop", 2, 899.99),
        ("Mouse", 5, 19.99),
        ("Tastiera", 3, 49.99),
        ("Monitor", 1, 299.99),
    ]
    
    total_generale = 0
    
    for product, qty, price in products:
        total = qty * price
        total_generale += total
        
        pdf.cell(60, 10, text=product, border=1)
        pdf.cell(40, 10, text=str(qty), border=1, align='C')
        pdf.cell(40, 10, text=f"€{price:.2f}", border=1, align='R')
        pdf.cell(40, 10, text=f"€{total:.2f}", border=1, new_x="LMARGIN", new_y="NEXT", align='R')
    
    # Totale
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(140, 10, text="TOTALE", border=1, align='R')
    pdf.cell(40, 10, text=f"€{total_generale:.2f}", border=1, align='R')
    
    pdf.output("../output/03_table_example.pdf")
    print("✓ PDF creato: output/03_table_example.pdf")

if __name__ == "__main__":
    create_table_pdf()
