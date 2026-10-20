
import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)

URL_PATTERN = re.compile(
    r"(?:https?://|www\.)[^\s<>\"']+",
    re.IGNORECASE,
)

PHONE_PATTERN = re.compile(
    r"(?<!\w)(?:\+?\d{1,3}[\s.-]?)?"
    r"(?:\(?\d{2,5}\)?[\s.-]?)?"
    r"\d{3,5}[\s.-]?\d{3,5}(?!\w)"
)


def _unique(values):
    """Keep the first occurrence of each value."""
    return list(dict.fromkeys(values))


def extract_contacts(text):
    """Extract contact details from resume text safely."""
    if not isinstance(text, str) or not text.strip():
        return {"emails": [], "phones": [], "urls": []}

    emails = _unique(EMAIL_PATTERN.findall(text))

    # Strip common punctuation that may follow a URL in prose.
    urls = _unique(
        match.rstrip(".,;:!?)\"]}")
        for match in URL_PATTERN.findall(text)
    )

    phones = []
    for match in PHONE_PATTERN.findall(text):
        digits = re.sub(r"\D", "", match)

        # Filter out short numbers and long numeric IDs.
        if 10 <= len(digits) <= 15:
            phones.append(match.strip())

    return {
        "emails": emails,
        "phones": _unique(phones),
        "urls": urls,
    }
