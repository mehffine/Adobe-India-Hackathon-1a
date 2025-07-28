import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

@dataclass
class ExtractorConfig:
    max_workers: int = 6
    batch_size_multiplier: int = 2
    heading_font_ratio: float = 1.15  # heading font ≥ body * ratio
    cache_size: int = 128             # LRU size

    def json_dumps(self, data: Dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    @classmethod
    def from_file(cls, fp: str | None) -> "ExtractorConfig":
        if not fp or not Path(fp).is_file():
            return cls()
        with open(fp, encoding="utf-8") as f:
            params = json.load(f)
        return cls(**params)
