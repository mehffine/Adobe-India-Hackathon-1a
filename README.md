# PDF Outline Extraction – Adobe Hackathon 2025

> **Challenge 1a: Structure Extraction from PDF (Title, H1/H2/H3)**

## 🚀 Approach

This solution uses an intelligent, multi-signal algorithm to accurately extract a hierarchical outline (Title, H1, H2, H3) from any PDF, including complex layouts and multilingual documents. It does _not_ rely solely on font size or appearance; instead, it weighs several cues to robustly identify headings (even when font size is unreliable).

The full pipeline is:

1. **Embedded TOC Extraction:**  
   If the PDF contains a machine-readable bookmarks/table-of-contents, these are parsed directly for high accuracy.

2. **Visual Analysis:**  
   If no TOC is present, each text line is scored for “heading likelihood” based on:
   - Font size (relative to body text, when available)
   - Boldness & capitalization
   - Margins and whitespace above (visual spacing clues)
   - Numbering patterns (e.g. "1.", "I.", "Chapter 1")
   - Frequency statistics of font/size combinations

3. **Scoring and Hierarchy:**  
   A weighted-sum heuristic assigns each line a “heading level” (H1, H2, H3). The final hierarchy keeps the natural order and page mappings.

**Result:**  
High-precision, schema-compliant outline extraction for both simple and challenging PDFs—without the need for any machine learning model or online service.

## 📦 Models & Libraries Used

- **[PyMuPDF (pymupdf)](https://github.com/pymupdf/PyMuPDF):**  
  For all PDF text, font, and layout extraction.
- **Python Standard Library:**  
  No external models, neural nets, or online accesses are used (fully open-source, lightweight, and offline).

> **No ML model is used** (model size is essentially zero). If desired, the heading scoring code can be replaced with a model ≤200MB for future rounds.

## 🛠️ How to Build and Run

> Your container is plug-and-play & works per the hackathon's **Expected Execution** section.

### **Build the Docker Image**

```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

_Replace `mysolutionname:somerandomidentifier` as desired._

### **Run (Batch Process All PDFs in Input Directory)**

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  mysolutionname:somerandomidentifier
```

- All PDF files in `./input` will be processed.
- Output JSON files will appear in `./output`, following the required naming.

## 📤 Output Example

Each processed PDF generates a JSON outline in this structure:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction",       "page": 1 },
    { "level": "H2", "text": "What is AI?",        "page": 2 },
    { "level": "H3", "text": "History of AI",      "page": 3 }
  ]
}
```

- **Keys and format** are strictly compliant with the challenge JSON schema.

## 🎯 Highlights

- **Not dependent on font size:** Robust multi-feature heading detection.
- **Multilingual:** Handles CJK, Arabic, etc., thanks to full Unicode support in PyMuPDF.
- **No network or external dependencies:** Works 100% offline. No model weights needed.
- **Scalable, Fast:** Designed to process 50-page PDFs within 10 seconds.
- **Docker/AMD64 ready** for reproducible, cross-environment execution.

## ℹ️ Notes

- If you wish to test locally:  
  `pip install pymupdf`  
  `python main.py -i input -o output`
- For **Docker**, no additional steps are required—just use the commands above.
