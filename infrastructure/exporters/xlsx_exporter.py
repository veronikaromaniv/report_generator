from openpyxl import Workbook
from infrastructure.exporters.base_exporter import BaseExporter
from domain.models import ReportData


class XLSXExporter(BaseExporter):
    """
    Експортер у формат Excel (XLSX).
    """

    def _render(self, data: ReportData, path: str):
        wb = Workbook()
        ws = wb.active
        ws.title = data.title

        # Заголовки
        ws.append(data.headers)

        # Рядки даних
        for row in data.rows:
            ws.append(row)

        wb.save(path)

    def _get_extension(self) -> str:
        return "xlsx"
