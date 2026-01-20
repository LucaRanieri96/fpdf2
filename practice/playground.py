from fpdf import FPDF

def my_experiment():
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('Helvetica', size=12)
    pdf.cell(text="Inizia a sperimentare qui!")
    
    # Il tuo codice qui...
    
    pdf.output("../output/playground.pdf")
    print("✓ PDF creato: output/playground.pdf")

if __name__ == "__main__":
    my_experiment()
