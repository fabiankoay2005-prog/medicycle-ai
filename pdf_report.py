from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(data, filename="medicycle_report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("MediCycle AI Hospital Report", styles["Title"]))
    content.append(Spacer(1, 12))

    for key, value in data.items():
        content.append(
            Paragraph(f"<b>{key}</b>: {value}", styles["Normal"])
        )
        content.append(Spacer(1, 8))

    doc.build(content)

    return filename