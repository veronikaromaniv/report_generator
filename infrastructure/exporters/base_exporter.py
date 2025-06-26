import os
import re
from abc import ABC, abstractmethod
from domain.models import ReportData


def slugify(text):
    """
    Замінює всі неалфавітні символи на підкреслення.
    Наприклад: "Test Report: June" -> "test_report_june"
    """
    return re.sub(r'[^a-zA-Z0-9_]+', '_', text).strip('_')


class BaseExporter(ABC):
    """
    Template Method: шаблон генерації звіту.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export(self, data: ReportData) -> str:
        """
        Шаблонний метод — не змінюється в підкласах.
        """
        filename = self._generate_filename(data)
        full_path = os.path.join(self.output_dir, filename)
        self._render(data, full_path)
        return full_path

    @abstractmethod
    def _render(self, data: ReportData, path: str):
        """
        Абстрактний метод для рендерингу звіту.
        """
        pass

    def _generate_filename(self, data: ReportData) -> str:
        name = slugify(data.title.lower())  # 👈 ОНОВЛЕНО
        return f"{name}.{self._get_extension()}"

    @abstractmethod
    def _get_extension(self) -> str:
        """
        Повертає розширення файлу (pdf, html, xlsx).
        """
        pass
