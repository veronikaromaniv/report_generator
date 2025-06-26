import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, TemplateSyntaxError, UndefinedError, StrictUndefined
from infrastructure.exporters.base_exporter import BaseExporter
from domain.models import ReportData


class HTMLExporter(BaseExporter):
    """
    Експортер у формат HTML (з шаблоном Jinja2).
    """

    def __init__(self, output_dir: str, template_dir: str):
        super().__init__(output_dir)
        self.template_dir = template_dir
        self.template_env = Environment(
            loader=FileSystemLoader(self.template_dir),
            undefined=StrictUndefined,
            auto_reload=True
        )

        # 🔍 Додаємо логування:
        print("[DEBUG] Templates folder:", self.template_env.loader.searchpath)
        print("[DEBUG] Looking for: report.html")

    def _render(self, data: ReportData, path: str):
        try:
            template = self.template_env.get_template("report.html")
        except TemplateNotFound:
            print("[ERROR] Template 'report.html' not found in the templates directory.")
            raise
        except TemplateSyntaxError as e:
            print(f"[ERROR] Syntax error in template: {e.message} at line {e.lineno}")
            raise
        except UndefinedError as e:
            print(f"[ERROR] Undefined variable in template: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Unexpected error while loading template: {e}")
            raise

        try:
            html_content = template.render(
                title=data.title,
                headers=data.headers,
                rows=data.rows,
                metadata=data.metadata  # додано
            )

        except Exception as e:
            print(f"[ERROR] Failed to render template: {e}")
            raise

        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _get_extension(self) -> str:
        return "html"
