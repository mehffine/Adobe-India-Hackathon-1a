from typing import Dict, Any, List

class HeadingClassifier:
    def __init__(self, body_font: float, ratio: float):
        self.body_font = body_font
        self.ratio = ratio

    def classify(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Label each item with heading level if font big enough."""
        out: List[Dict[str, Any]] = []
        for it in items:
            size = it["size"]
            if size >= self.body_font * self.ratio:
                level = self._level(size)
                out.append({"level": level, "text": it["text"], "page": it["page"]})
        return out

    def _level(self, size: float) -> str:
        rel = size / self.body_font
        if rel > 2.0:
            return "H1"
        if rel > 1.6:
            return "H2"
        if rel > 1.3:
            return "H3"
        return "H4"
