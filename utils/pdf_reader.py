"""
Extract plain text from PDF files.
Uses PyMuPDF (fitz) if available, falls back to pdfminer.
"""

import importlib


def extract_text_from_pdf(filepath: str) -> str:
    """Return the full text content of a PDF file."""

    # Try PyMuPDF first (fastest)
    fitz = importlib.import_module("fitz") if _has("fitz") else None
    if fitz:
        doc = fitz.open(filepath)
        pages = [page.get_text() for page in doc]
        doc.close()
        text = "\n".join(pages)
        if text.strip():
            return text

    # Fallback: pypdf
    pypdf = importlib.import_module("pypdf") if _has("pypdf") else None
    if pypdf:
        reader = pypdf.PdfReader(filepath)
        pages = [p.extract_text() or "" for p in reader.pages]
        text = "\n".join(pages)
        if text.strip():
            return text

    raise RuntimeError(
        "Could not extract text from PDF.\n"
        "Install PyMuPDF:  pip install pymupdf\n"
        "or pypdf:         pip install pypdf"
    )


def _has(module_name: str) -> bool:
    import importlib.util
    return importlib.util.find_spec(module_name) is not None
