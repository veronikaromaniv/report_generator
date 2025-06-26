import os
from application.factory import ExporterFactory
from application.report_service import ReportService
from domain.models import ReportData


def run_demo():
    # ✅ Дані для прикладу
    data = ReportData(
        title="June Sales",
        metadata={"author": "Veronica", "date": "2025-06-25"},
        headers=["Product", "Quantity", "Price"],
        rows=[
            ["Laptop", 5, "25000"],
            ["Smartphone", 10, "15000"],
            ["Tablet", 3, "12000"]
        ]
    )

    # ✅ Шляхи
    base_dir = os.path.dirname(__file__)
    template_dir = os.path.join(base_dir, "interface", "templates")
    output_dir = os.path.join(base_dir, "out")

    print(f"[DEBUG] Template dir: {template_dir}")
    print(f"[DEBUG] Output dir: {output_dir}")

    # 🏭 Фабрика та сервіс
    factory = ExporterFactory(output_dir=output_dir, template_dir=template_dir)
    service = ReportService(factory)

    # 🔁 Генерація у 3 формати
    for fmt in ["pdf", "html", "xlsx"]:
        try:
            path = service.generate_report(data, fmt)
            print(f"✅ Звіт збережено: {path}")
        except Exception as e:
            print(f"❌ Помилка при генерації {fmt}: {e}")


if __name__ == "__main__":
    run_demo()
