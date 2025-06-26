import os
import pytest

from infrastructure.exporters.html_exporter import HTMLExporter
from domain.models import ReportData
from jinja2 import TemplateNotFound, TemplateSyntaxError, UndefinedError


# --- Фікстура даних ---
@pytest.fixture
def sample_data():
    return ReportData(
        title="Sample",
        headers=["Name", "Score"],
        rows=[["Alice", "95"]],
        metadata={"author": "Test", "date": "2025-06-25"}
    )


# --- Тест: шаблон не знайдено ---
def test_template_not_found(tmp_path, sample_data):
    broken_template_dir = os.path.abspath("tests/broken_templates")
    exporter = HTMLExporter(output_dir=str(tmp_path), template_dir=broken_template_dir)

    with pytest.raises(TemplateNotFound):
        exporter.export(sample_data)


# --- Тест: синтаксична помилка у шаблоні ---
def test_template_syntax_error(tmp_path, sample_data):
    invalid_template_dir = os.path.abspath("tests/invalid_templates")
    exporter = HTMLExporter(output_dir=str(tmp_path), template_dir=invalid_template_dir)

    with pytest.raises(TemplateSyntaxError):
        exporter.export(sample_data)


# --- Тест: змінна у шаблоні не визначена ---
def test_template_undefined_variable(tmp_path, sample_data):
    undefined_var_template_dir = os.path.abspath("tests/templates_with_undefined_var")
    exporter = HTMLExporter(output_dir=str(tmp_path), template_dir=undefined_var_template_dir)

    with pytest.raises(UndefinedError):
        exporter.export(sample_data)


# --- Тест: валідний шаблон рендериться без помилок ---
def test_template_valid(tmp_path, sample_data):
    valid_template_dir = os.path.abspath("interface/templates")
    exporter = HTMLExporter(output_dir=str(tmp_path), template_dir=valid_template_dir)

    output_path = exporter.export(sample_data)
    assert os.path.exists(output_path)
    assert output_path.endswith(".html")


# --- Додатково: загальна помилка при get_template() ---
def test_general_exception_get_template(tmp_path, sample_data, monkeypatch):
    exporter = HTMLExporter(output_dir=str(tmp_path), template_dir="interface/templates")

    def raise_general(*args, **kwargs):
        raise Exception("Simulated general failure in get_template")

    monkeypatch.setattr(exporter.template_env, "get_template", raise_general)

    with pytest.raises(Exception, match="Simulated general failure in get_template"):
        exporter.export(sample_data)


# --- Додатково: помилка при render() ---
def test_render_raises_exception(tmp_path, sample_data, monkeypatch):
    class FakeTemplate:
        def render(self, **kwargs):
            raise Exception("Render failed")

    exporter = HTMLExporter(output_dir=str(tmp_path), template_dir="interface/templates")
    monkeypatch.setattr(exporter.template_env, "get_template", lambda name: FakeTemplate())

    with pytest.raises(Exception, match="Render failed"):
        exporter.export(sample_data)
