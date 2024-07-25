from fpdf import FPDF
import io

def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.cell(200, 10, txt="Produk Terpopuler", ln=True, align='C')

    # Column titles
    pdf.cell(100, 10, txt="Kata", border=1)
    pdf.cell(100, 10, txt="Jumlah", border=1, ln=True)

    # Data rows
    for index, row in df.iterrows():
        pdf.cell(100, 10, txt=str(row['Kata']), border=1)
        pdf.cell(100, 10, txt=str(row['Jumlah']), border=1, ln=True)

    # Save to BytesIO and return as bytes
    pdf_output = io.BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))  # 'S' is for string mode, to get PDF as bytes
    pdf_output.seek(0)  # Go to the start of the BytesIO object
    return pdf_output.getvalue()  # Return the bytes