
from pathlib import Path

from src.resume_analyzer.pipeline import process_resume
from src.resume_analyzer.contact_extractor import extract_contacts
from src.resume_analyzer.entity_extractor import extract_entities
from src.resume_analyzer.skill_extractor import extract_skills


class ResumeParser:
    """Integrate resume text processing and information extraction."""

    def parsefile(self, file_path: str | Path) -> dict:
        """Parse a PDF or DOCX resume into a structured dictionary."""
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"Resume file not found: {path}")

        if path.suffix.lower() not in {".pdf", ".docx"}:
            raise ValueError("Unsupported file type. Upload a PDF or DOCX file.")

        # Reuse the existing Day 2 pipeline.
        result = process_resume(path)

        raw_text = result.get("raw_text", "")
        cleaned_text = result.get("cleaned_text", "")

        # Supply safe defaults for missing text fields.
        if not isinstance(raw_text, str):
            raw_text = ""
        if not isinstance(cleaned_text, str):
            cleaned_text = ""

        errors = []

        # Run contact extraction independently.
        try:
            contacts = extract_contacts(cleaned_text)
        except Exception as exc:
            contacts = {"emails": [], "phones": [], "urls": []}
            errors.append(f"Contact extraction failed: {exc}")

        # Run named entity extraction independently.
        try:
            entities = extract_entities(cleaned_text)
        except Exception as exc:
            entities = {
                "persons": [],
                "organizations": [],
                "locations": [],
                "dates": [],
            }
            errors.append(f"Entity extraction failed: {exc}")

        # Run skill extraction independently.
        try:
            skills = extract_skills(cleaned_text)
        except Exception as exc:
            skills = []
            errors.append(f"Skill extraction failed: {exc}")

        persons = entities.get("persons", [])

        return {
            "status": "success" if not errors else "partial_success",
            "file_name": path.name,
            "contact": contacts,
            "candidate": {
                "name": persons[0] if persons else None,
                "entities": entities,
            },
            "skills": skills,
            "sections": result.get("sections", {}),
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "errors": errors,
        }


def parsefile(file_path: str | Path) -> dict:
    """Convenience function for parsing a resume."""
    return ResumeParser().parsefile(file_path)
