from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ReportData:
    """
    Модель даних звіту, яку обробляє генератор.
    """
    title: str
    headers: List[str]
    rows: List[List[str]]
    metadata: Dict[str, str] = None
