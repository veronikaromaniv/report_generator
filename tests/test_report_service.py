import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from application.factory import ExporterFactory
from application.report_service import ReportService
from domain.models import ReportData


# --- Фікстури ---

@pytest.fixture
def sample_data():
    return ReportData(
        title="Test Report",
        headers=["Name", "Score"],
        rows=[
            ["Alice", "95"],
            ["Bob", "88"]
        ],
        metadata={"author": "Test", "date": "2025-06-25"}
    )


@pytest.fixture
def template_dir():
    return os.path.abspath("interface/templates")


# --- Генерація звітів у кожному форматі окремо ---

def test_generate_pdf_report(tmp_path, sample_data):
    factory = ExporterFactory(output_dir=str(tmp_path))
    service = ReportService(factory)
    path = service.generate_report(sample_data, "pdf")
    assert os.path.isfile(path)
    assert path.endswith(".pdf")


def test_generate_html_report(tmp_path, sample_data, template_dir):
    factory = ExporterFactory(output_dir=str(tmp_path), template_dir=template_dir)
    service = ReportService(factory)
    path = service.generate_report(sample_data, "html")
    assert os.path.isfile(path)
    assert path.endswith(".html")


def test_generate_xlsx_report(tmp_path, sample_data):
    factory = ExporterFactory(output_dir=str(tmp_path))
    service = ReportService(factory)
    path = service.generate_report(sample_data, "xlsx")
    assert os.path.isfile(path)
    assert path.endswith(".xlsx")


# --- Тести фабрики ---

def test_factory_returns_pdf(tmp_path, template_dir):
    factory = ExporterFactory(output_dir=str(tmp_path), template_dir=template_dir)
    exporter = factory.create_exporter("pdf")
    assert exporter.__class__.__name__ == "PDFExporter"


def test_factory_returns_html(tmp_path, template_dir):
    factory = ExporterFactory(output_dir=str(tmp_path), template_dir=template_dir)
    exporter = factory.create_exporter("html")
    assert exporter.__class__.__name__ == "HTMLExporter"


def test_factory_returns_xlsx(tmp_path, template_dir):
    factory = ExporterFactory(output_dir=str(tmp_path), template_dir=template_dir)
    exporter = factory.create_exporter("xlsx")
    assert exporter.__class__.__name__ == "XLSXExporter"


def test_factory_invalid_format_raises(tmp_path, template_dir):
    factory = ExporterFactory(output_dir=str(tmp_path), template_dir=template_dir)
    with pytest.raises(ValueError):
        factory.create_exporter("unknown")


# --- Тести ReportData ---

def test_reportdata_metadata(sample_data):
    assert sample_data.metadata["author"] == "Test"


def test_reportdata_title(sample_data):
    assert sample_data.title == "Test Report"


def test_reportdata_headers(sample_data):
    assert sample_data.headers == ["Name", "Score"]


def test_reportdata_rows_count(sample_data):
    assert len(sample_data.rows) == 2


def test_reportdata_row_content(sample_data):
    assert sample_data.rows[0] == ["Alice", "95"]
    assert sample_data.rows[1][1] == "88"


# --- Негативні кейси / додаткові ---

def test_invalid_format_in_service_raises(tmp_path, sample_data):
    factory = ExporterFactory(output_dir=str(tmp_path))
    service = ReportService(factory)
    with pytest.raises(ValueError):
        service.generate_report(sample_data, "docx")


def test_empty_data_report(tmp_path):
    data = ReportData(title="Empty", headers=[], rows=[], metadata={})
    factory = ExporterFactory(output_dir=str(tmp_path))
    service = ReportService(factory)
    path = service.generate_report(data, "pdf")
    assert os.path.exists(path)


def test_title_slugified_correctly(tmp_path):
    data = ReportData(title="Test Report: June", headers=["A"], rows=[["B"]], metadata={})
    factory = ExporterFactory(output_dir=str(tmp_path))
    service = ReportService(factory)
    path = service.generate_report(data, "pdf")
    assert "test_report_june" in os.path.basename(path).lower()


def test_output_directory_created(tmp_path, sample_data):
    output_dir = str(tmp_path / "custom_out")
    factory = ExporterFactory(output_dir=output_dir)
    service = ReportService(factory)
    path = service.generate_report(sample_data, "pdf")
    assert os.path.isdir(output_dir)
    assert os.path.exists(path)


# --- Додаткові тести (щоб було 20) ---

def test_html_report_contains_title(tmp_path, sample_data, template_dir):
    factory = ExporterFactory(output_dir=str(tmp_path), template_dir=template_dir)
    service = ReportService(factory)
    path = service.generate_report(sample_data, "html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Test Report" in content


def test_pdf_report_nonzero_size(tmp_path, sample_data):
    factory = ExporterFactory(output_dir=str(tmp_path))
    service = ReportService(factory)
    path = service.generate_report(sample_data, "pdf")
    assert os.path.getsize(path) > 0


def test_xlsx_report_extension(tmp_path, sample_data):
    factory = ExporterFactory(output_dir=str(tmp_path))
    service = ReportService(factory)
    path = service.generate_report(sample_data, "xlsx")
    assert path.endswith(".xlsx")


def test_metadata_in_html_report(tmp_path, template_dir):
    data = ReportData(
        title="Meta Report",
        headers=["X"],
        rows=[["Y"]],
        metadata={"author": "Verona", "date": "2025-06-25"}
    )
    factory = ExporterFactory(output_dir=str(tmp_path), template_dir=template_dir)
    service = ReportService(factory)
    path = service.generate_report(data, "html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Verona" in content
    assert "2025-06-25" in content
