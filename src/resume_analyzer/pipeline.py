
from pathlib import Path

from .cleaner import clean_text
from .extractor import extract_text
from .segmenter import segment_sections


def process_resume(file_path: str | Path) -> dict:
    """Extract, clean and segment a resume."""
    raw_text = extract_text(file_path)
    cleaned_text = clean_text(raw_text)
    sections = segment_sections(cleaned_text)

    return {
        "file_name": Path(file_path).name,
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "sections": sections,
    }
