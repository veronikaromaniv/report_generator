from infrastructure.exporters.base_exporter import BaseExporter
from infrastructure.exporters.pdf_exporter import PDFExporter
from infrastructure.exporters.html_exporter import HTMLExporter
from infrastructure.exporters.xlsx_exporter import XLSXExporter


class ExporterFactory:
    """
    Factory Method: створює потрібний експортер за вказаним форматом.
    """

    def __init__(self, output_dir: str, template_dir: str = None):
        self.output_dir = output_dir
        self.template_dir = template_dir

    def create_exporter(self, format: str) -> BaseExporter:
        format = format.lower()
        if format == "pdf":
            return PDFExporter(self.output_dir)
        elif format == "html":
            return HTMLExporter(self.output_dir, self.template_dir)
        elif format == "xlsx":
            return XLSXExporter(self.output_dir)
        else:
            raise ValueError(f"Unsupported format: {format}")
