import re
from typing import List, Dict, Any

class TextProcessor:
    _whitespace = re.compile(r"\s+")
    _noise = re.compile(r"^(\d+|Page\s+\d+)$", re.I)

    @classmethod
    def clean(cls, s: str) -> str:
        s = cls._whitespace.sub(" ", s).strip()
        return s

    @classmethod
    def filter_lines(cls, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove headers, footers, page numbers."""
        return [it for it in items if not cls._noise.match(it["text"])]
