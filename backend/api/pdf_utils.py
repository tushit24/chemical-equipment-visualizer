from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_dataset_pdf(dataset):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Chemical Equipment Dataset Report")

    c.setFont("Helvetica", 12)
    y -= 40
    c.drawString(50, y, f"Filename: {dataset.filename}")

    y -= 25
    c.drawString(50, y, f"Total Equipment: {dataset.total_equipment}")

    y -= 25
    c.drawString(50, y, f"Average Flowrate: {dataset.average_flowrate}")

    y -= 25
    c.drawString(50, y, f"Average Pressure: {dataset.average_pressure}")

    y -= 25
    c.drawString(50, y, f"Average Temperature: {dataset.average_temperature}")

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Equipment Type Distribution:")

    c.setFont("Helvetica", 12)
    y -= 25

    for eq_type, count in dataset.type_distribution.items():
        c.drawString(70, y, f"{eq_type}: {count}")
        y -= 20

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
