
import re


def clean_text(text: str) -> str:
    """Normalize extracted text while preserving useful content."""
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    # Normalize Windows and old-style line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove null bytes sometimes found in extracted documents.
    text = text.replace("\x00", "")

    # Remove trailing spaces on each line.
    lines = [line.strip() for line in text.split("\n")]

    # Collapse repeated spaces and tabs without joining lines.
    lines = [re.sub(r"[ \t]+", " ", line) for line in lines]

    text = "\n".join(lines)

    # Limit excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
