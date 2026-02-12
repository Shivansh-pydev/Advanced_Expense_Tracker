from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def create_pdf(file_path, df):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    elements = []
    elements.append(Paragraph("Expense Report", styles['Title']))
    elements.append(Spacer(1,12))

    total = df['Amount'].sum()
    elements.append(Paragraph(f"Total Expense: ₹{round(total,2)}", styles['Normal']))
    elements.append(Spacer(1,12))

    for _, row in df.iterrows():
        text = f"{row['Date']} - {row['Category']} - ₹{row['Amount']} - {row['Note']}"
        elements.append(Paragraph(text, styles['Normal']))

    doc.build(elements)
    return file_path
