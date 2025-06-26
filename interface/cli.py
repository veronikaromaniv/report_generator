import os
import argparse
from domain.models import ReportData
from application.factory import ExporterFactory
from application.report_service import ReportService


def main():
    parser = argparse.ArgumentParser(description="Report Generator CLI")
    parser.add_argument("--format", required=True, help="Формат звіту: pdf/html/xlsx")
    parser.add_argument("--output", default="out", help="Каталог для збереження файлу")
    parser.add_argument("--templates", default="report_generator/interface/templates", help="Шлях до HTML-шаблонів")
    args = parser.parse_args()

    # Пример даних
    data = ReportData(
        title="Приклад звіту",
        headers=["Ім'я", "Прізвище", "Бал"],
        rows=[
            ["Анна", "Іванова", "95"],
            ["Богдан", "Петренко", "88"],
            ["Катерина", "Коваль", "91"],
        ],
        metadata={"author": "Veronika", "date": "2025-06-25"}
    )

    factory = ExporterFactory(output_dir=args.output, template_dir=args.templates)
    service = ReportService(factory)
    result_path = service.generate_report(data, args.format)

    print(f"\n✅ Звіт успішно збережено в: {result_path}")


if __name__ == "__main__":
    main()
