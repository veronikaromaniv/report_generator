from domain.models import ReportData
from application.factory import ExporterFactory


class ReportService:
    """
    Сервіс для генерації звітів у різних форматах.
    """

    def __init__(self, factory: ExporterFactory):
        self.factory = factory

    def generate_report(self, data: ReportData, format: str) -> str:
        """
        Генерує звіт у заданому форматі.
        :param data: вхідні дані
        :param format: формат звіту (pdf/html/xlsx)
        :return: шлях до згенерованого файлу
        """
        exporter = self.factory.create_exporter(format)
        return exporter.export(data)
