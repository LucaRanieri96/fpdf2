"""
Esempio 5: Forme e Colori
Disegnare linee, rettangoli, cerchi con colori
"""
from fpdf import FPDF

def create_shapes_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Titolo
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, text='Forme e Colori', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    
    # Linee
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, text='Linee:', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_line_width(0.5)
    pdf.line(20, 40, 190, 40)  # Linea orizzontale
    
    pdf.set_line_width(1)
    pdf.set_draw_color(255, 0, 0)  # Rosso
    pdf.line(20, 45, 190, 45)
    
    pdf.set_line_width(2)
    pdf.set_draw_color(0, 0, 255)  # Blu
    pdf.line(20, 52, 190, 52)
    
    pdf.ln(25)
    
    # Rettangoli
    pdf.set_draw_color(0, 0, 0)  # Nero
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, text='Rettangoli:', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    # Rettangolo con solo bordo
    pdf.set_line_width(0.5)
    pdf.rect(20, 80, 40, 30)
    
    # Rettangolo riempito
    pdf.set_fill_color(255, 200, 200)  # Rosa
    pdf.rect(70, 80, 40, 30, 'F')
    
    # Rettangolo con bordo e riempimento
    pdf.set_fill_color(200, 255, 200)  # Verde chiaro
    pdf.set_draw_color(0, 128, 0)  # Verde scuro
    pdf.set_line_width(1)
    pdf.rect(120, 80, 40, 30, 'DF')
    
    pdf.ln(45)
    
    # Cerchi (ellissi)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, text='Cerchi:', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    # Cerchio con solo bordo
    pdf.set_line_width(0.5)
    pdf.ellipse(40, 145, 15, 15)
    
    # Cerchio riempito
    pdf.set_fill_color(255, 255, 200)  # Giallo
    pdf.ellipse(90, 145, 15, 15, 'F')
    
    # Cerchio con bordo e riempimento
    pdf.set_fill_color(200, 200, 255)  # Azzurro
    pdf.set_draw_color(0, 0, 255)  # Blu
    pdf.set_line_width(1)
    pdf.ellipse(140, 145, 15, 15, 'DF')
    
    pdf.ln(30)
    
    # Box colorato con testo
    pdf.set_fill_color(70, 130, 180)  # Steel blue
    pdf.set_text_color(255, 255, 255)  # Bianco
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 15, text='Box con Testo Colorato', fill=True, align='C')
    
    pdf.output("../output/05_shapes_and_colors.pdf")
    print("✓ PDF creato: output/05_shapes_and_colors.pdf")

if __name__ == "__main__":
    create_shapes_pdf()
