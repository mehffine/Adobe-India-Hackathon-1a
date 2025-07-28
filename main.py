#!/usr/bin/env python3
"""
Adobe India Hackathon 2025 – Challenge 1a
"""
import argparse, logging, multiprocessing, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple

from src.config import ExtractorConfig
from src.pdf_extractor import PDFOutlineExtractor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()]
)
log = logging.getLogger(__name__)


class RobustPDFProcessor:
    def __init__(self, cfg: ExtractorConfig):
        self.cfg = cfg
        self.extractor = PDFOutlineExtractor(cfg)

    def _process_one(self, pdf: Path, out_dir: Path) -> Tuple[str, float, bool]:
        start = time.time()
        try:
            data = self.extractor.extract_outline(pdf)
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"{pdf.stem}.json").write_text(
                self.cfg.json_dumps(data), encoding="utf-8"
            )
            return pdf.name, time.time() - start, True
        except Exception as exc:                                   # noqa
            log.error("Failed %s – %s", pdf.name, exc)
            return pdf.name, time.time() - start, False

    def run(self, in_dir: Path, out_dir: Path) -> None:
        pdfs = list(in_dir.glob("*.pdf"))
        if not pdfs:
            log.warning("No PDFs in %s", in_dir)
            return
        workers = min(6, multiprocessing.cpu_count(), len(pdfs))
        with ThreadPoolExecutor(workers) as pool:
            futures = [pool.submit(self._process_one, p, out_dir) for p in pdfs]
            ok = 0
            for f in as_completed(futures):
                name, dur, succ = f.result()
                log.info("%s → %.2fs %s", name, dur, "✓" if succ else "✗")
                ok += succ
        log.info("Summary: %d/%d succeeded", ok, len(pdfs))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="input", help="PDF folder")
    ap.add_argument("-o", "--output", default="output", help="JSON folder")
    ap.add_argument("-c", "--config", help="Optional config JSON")
    args = ap.parse_args()

    cfg = ExtractorConfig.from_file(args.config) if args.config else ExtractorConfig()
    RobustPDFProcessor(cfg).run(Path(args.input), Path(args.output))


if __name__ == "__main__":
    main()
