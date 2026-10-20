
"""Resume analyzer package."""

from .contact_extractor import extract_contacts
from .entity_extractor import extract_entities
from .skill_extractor import extract_skills


def analyze_resume_text(text):
    """Run the Day 2 extraction modules on resume text."""
    if not isinstance(text, str):
        text = ""

    return {
        "contacts": extract_contacts(text),
        "entities": extract_entities(text),
        "skills": extract_skills(text),
    }
