
import re


SECTION_ALIASES = {
    "contact": [
        "contact",
        "contact information",
        "personal details",
    ],
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "career objective",
        "objective",
        "about me",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "key skills",
        "technologies",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
    ],
    "education": [
        "education",
        "academic background",
        "educational qualifications",
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses and certifications",
    ],
    "achievements": [
        "achievements",
        "awards",
        "honors",
        "accomplishments",
    ],
}


def normalize_heading(line: str) -> str:
    """Normalize a potential section heading."""
    line = line.strip().lower()
    line = re.sub(r"[:\s]+$", "", line)
    line = re.sub(r"\s+", " ", line)
    return line


HEADING_LOOKUP = {
    normalize_heading(alias): section
    for section, aliases in SECTION_ALIASES.items()
    for alias in aliases
}


def segment_sections(text: str) -> dict[str, str]:
    """Group resume lines under recognized section headings."""
    sections = {"other": []}
    current_section = "other"

    for line in text.splitlines():
        heading = normalize_heading(line)

        # Remove common Markdown heading markers.
        heading = re.sub(r"^#+\s*", "", heading)

        # Handle common colon-ended headings.
        section = HEADING_LOOKUP.get(heading)

        if section:
            current_section = section
            sections.setdefault(current_section, [])
            continue

        sections.setdefault(current_section, []).append(line)

    return {
        name: "\n".join(lines).strip()
        for name, lines in sections.items()
        if "\n".join(lines).strip()
    }
