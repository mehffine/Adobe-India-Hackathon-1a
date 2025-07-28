from pathlib import Path
from typing import Dict, List
import fitz                                    # PyMuPDF

from .config import ExtractorConfig
from .cache_manager import cached
from .text_processor import TextProcessor
from .heading_classifier import HeadingClassifier
from .outline_hierarchy import OutlineHierarchy

class PDFOutlineExtractor:
    def __init__(self, cfg: ExtractorConfig):
        self.cfg = cfg

    def extract_outline(self, pdf_path: Path | str) -> Dict:
        doc = fitz.open(pdf_path)
        title = doc.metadata.get("title") or Path(pdf_path).stem

        toc = doc.get_toc(simple=True)
        if toc:
            outline = [
                {"level": f"H{lvl}", "text": title_, "page": page}
                for lvl, title_, page in toc
            ]
            return {"title": title, "outline": outline}

        # fallback: intelligent analysis
        items = self._analyze_pages(doc)
        body_font = self._median_font(items)
        headings = HeadingClassifier(body_font, self.cfg.heading_font_ratio).classify(
            items
        )
        outline = OutlineHierarchy.build(headings)
        return {"title": title, "outline": outline}

    # ---------- helpers ---------- #
    @cached(maxsize=32)
    def _analyze_pages(self, doc) -> List[Dict]:
        out: List[Dict] = []
        for page_index, pg in enumerate(doc, 1):
           for blk in pg.get_text("dict")["blocks"]:
                if blk.get("type") != 0 or "lines" not in blk:
                    continue
                for line in blk["lines"]:
                    text = " ".join(sp["text"] for sp in line["spans"]).strip()
                    if not text:
                        continue
                    size = line["spans"][0]["size"]
                    out.append({"text": TextProcessor.clean(text),
                                "size": size,
                                "page": page_index})
        return TextProcessor.filter_lines(out)

    @staticmethod
    def _median_font(items) -> float:
        sizes = sorted(it["size"] for it in items)
        n = len(sizes)
        return (sizes[n // 2] if n % 2 else (sizes[n // 2 - 1] + sizes[n // 2]) / 2)
