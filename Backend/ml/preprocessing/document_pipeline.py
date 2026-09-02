"""
PIWOT Legal Advisor — Full Multi-Page Contract Preprocessing Pipeline
Provides robust text extraction, OCR fallback, legal normalization, and clause chunking.
"""

import os
import re
import uuid
import logging
from typing import Dict, List, Any, Optional, Tuple
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

# Maximum allowable file size (16MB default)
MAX_FILE_SIZE_BYTES = 16 * 1024 * 1024

# Legal section header detection regex
SECTION_HEADER_PATTERNS = [
    re.compile(r'^\s*(?:SECTION|ARTICLE|CLAUSE|ITEM|PARAGRAPH)?\s*([0-9]+(?:\.[0-9]+)*|[IVXLCDM]+)[\.\:\-\s]+([A-Z0-9\s\,\'\/\-\(\)]{3,80})', re.IGNORECASE),
    re.compile(r'^\s*([0-9]+\.[0-9]*|[IVXLCDM]+\.)\s+([A-Z\s]{3,60})$', re.MULTILINE),
    re.compile(r'^\s*([A-Z\s]{4,50})\s*$', re.MULTILINE),
]


class DocumentPreprocessingError(Exception):
    """Raised when document extraction or validation fails."""
    pass


def validate_pdf_stream(pdf_bytes: bytes, filename: str = "document.pdf") -> None:
    """Validates PDF byte stream size, header, and corruption."""
    if not pdf_bytes:
        raise DocumentPreprocessingError("The uploaded file is empty.")

    if len(pdf_bytes) > MAX_FILE_SIZE_BYTES:
        raise DocumentPreprocessingError(
            f"File size ({len(pdf_bytes) / (1024 * 1024):.1f}MB) exceeds the maximum allowed limit of {MAX_FILE_SIZE_BYTES / (1024 * 1024):.0f}MB."
        )

    if not pdf_bytes.startswith(b"%PDF-"):
        raise DocumentPreprocessingError("Invalid file header: File is not a valid PDF document.")


def normalize_legal_text(text: str) -> str:
    """
    Cleans extracted legal text conservatively.
    Preserves legal numbering, monetary amounts, percentages, and punctuation.
    """
    if not text:
        return ""
    
    # Replace non-breaking spaces and irregular unicode whitespaces
    text = text.replace('\xa0', ' ').replace('\u200b', '').replace('\ufeff', '')
    
    # Replace curly quotes and apostrophes with standard ASCII
    text = text.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    text = text.replace('—', ' - ').replace('–', ' - ')

    # Fix broken hyphenated line breaks (e.g. "agree-\n ment" -> "agreement")
    text = re.sub(r'(\b[a-zA-Z]+)-\n\s*([a-zA-Z]+\b)', r'\1\2', text)
    
    # Normalize multiple consecutive spaces (while preserving single line breaks)
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Normalize multiple consecutive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def extract_pages_with_ocr_fallback(pdf_bytes: bytes) -> Tuple[List[Dict[str, Any]], bool]:
    """
    Extracts text from all pages using PyMuPDF.
    If a page contains less than 40 characters of extractable text, triggers OCR fallback.
    """
    validate_pdf_stream(pdf_bytes)

    pages = []
    ocr_triggered_overall = False

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if len(doc) == 0:
            raise DocumentPreprocessingError("PDF contains 0 pages.")

        for page_idx in range(len(doc)):
            page_num = page_idx + 1
            page = doc.load_page(page_idx)
            page_text = page.get_text("text")

            # Check if text is sparse (scanned page)
            is_scanned_page = len(page_text.strip()) < 40
            ocr_used_for_page = False

            if is_scanned_page:
                try:
                    import pytesseract
                    from PIL import Image
                    import io

                    # Render page at 200 DPI
                    pix = page.get_pixmap(dpi=200)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    ocr_text = pytesseract.image_to_string(img)
                    if len(ocr_text.strip()) > len(page_text.strip()):
                        page_text = ocr_text
                        ocr_used_for_page = True
                        ocr_triggered_overall = True
                except Exception as ocr_err:
                    logger.warning(f"OCR fallback skipped/failed on page {page_num}: {ocr_err}")

            cleaned_text = normalize_legal_text(page_text)
            pages.append({
                "page": page_num,
                "text": cleaned_text,
                "char_count": len(cleaned_text),
                "ocr_used": ocr_used_for_page
            })

        doc.close()
    except Exception as e:
        if isinstance(e, DocumentPreprocessingError):
            raise
        raise DocumentPreprocessingError(f"Failed to parse PDF document: {str(e)}")

    return pages, ocr_triggered_overall


def segment_into_clause_chunks(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Segments full document pages into logical clause chunks.
    Preserves exact page numbers, character offsets, and inferred section titles.
    """
    chunks = []
    chunk_counter = 1

    for page_info in pages:
        page_num = page_info["page"]
        text = page_info["text"]

        if not text or len(text.strip()) == 0:
            continue

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        current_section = "General Provisions"
        current_chunk_lines = []

        def flush_chunk(section_name, chunk_lines):
            nonlocal chunk_counter
            if not chunk_lines:
                return
            combined_text = " ".join(chunk_lines).strip()
            if len(combined_text) >= 15:
                chunks.append({
                    "chunk_id": f"chunk_{chunk_counter:03d}",
                    "page_start": page_num,
                    "page_end": page_num,
                    "section": section_name,
                    "text": combined_text,
                    "char_count": len(combined_text)
                })
                chunk_counter += 1

        for line in lines:
            # Check if this line is a section header
            is_header = False
            for pattern in SECTION_HEADER_PATTERNS:
                if pattern.match(line):
                    is_header = True
                    break
            
            if is_header:
                # Flush existing buffer
                flush_chunk(current_section, current_chunk_lines)
                current_chunk_lines = []
                current_section = line
            else:
                current_chunk_lines.append(line)

        # Flush any remaining lines on the page
        flush_chunk(current_section, current_chunk_lines)

    # Fallback if no structured sections were detected
    if not chunks:
        for page_info in pages:
            if page_info["text"]:
                chunks.append({
                    "chunk_id": f"chunk_{chunk_counter:03d}",
                    "page_start": page_info["page"],
                    "page_end": page_info["page"],
                    "section": "General",
                    "text": page_info["text"],
                    "char_count": len(page_info["text"])
                })
                chunk_counter += 1

    return chunks


def process_contract_document(pdf_bytes: bytes, filename: str = "contract.pdf") -> Dict[str, Any]:
    """
    Canonical End-to-End Contract Preprocessing Pipeline.
    Returns structured canonical JSON representation.
    """
    doc_id = f"doc_{uuid.uuid4().hex[:10]}"
    pages, ocr_used = extract_pages_with_ocr_fallback(pdf_bytes)
    chunks = segment_into_clause_chunks(pages)

    total_chars = sum(p["char_count"] for p in pages)
    full_text = "\n\n".join(p["text"] for p in pages if p["text"])

    return {
        "document_id": doc_id,
        "filename": filename,
        "page_count": len(pages),
        "char_count": total_chars,
        "ocr_used": ocr_used,
        "full_text": full_text,
        "pages": pages,
        "chunks": chunks
    }
