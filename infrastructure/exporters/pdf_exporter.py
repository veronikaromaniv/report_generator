from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from infrastructure.exporters.base_exporter import BaseExporter
from domain.models import ReportData


class PDFExporter(BaseExporter):
    """
    Експортер у формат PDF.
    """

    def _render(self, data: ReportData, path: str):
        c = canvas.Canvas(path, pagesize=A4)
        width, height = A4

        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, data.title)

        y -= 30
        c.setFont("Helvetica", 10)

        # headers
        for i, header in enumerate(data.headers):
            c.drawString(50 + i * 100, y, header)

        y -= 20

        # rows
        for row in data.rows:
            for i, cell in enumerate(row):
                c.drawString(50 + i * 100, y, str(cell))
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50

        c.save()

    def _get_extension(self) -> str:
        return "pdf"