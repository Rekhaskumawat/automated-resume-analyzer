
import json
import re
from pathlib import Path


DEFAULT_SKILLS_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "skills.json"
)


def load_skills(skills_path=None):
    """Load canonical skills and aliases from JSON."""
    path = Path(skills_path) if skills_path else DEFAULT_SKILLS_PATH

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Skills file not found: {path}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in skills file: {path}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError("skills.json must contain a JSON object")

    for skill, aliases in data.items():
        if not isinstance(skill, str) or not skill.strip():
            raise ValueError("Each canonical skill must be a non-empty string")
        if not isinstance(aliases, list) or not all(
            isinstance(alias, str) and alias.strip()
            for alias in aliases
        ):
            raise ValueError(
                f"Aliases for '{skill}' must be a list of non-empty strings"
            )

    return data


def _contains_term(text, term):
    """Match a phrase without matching inside unrelated words."""
    pattern = (
        r"(?<!\w)" + re.escape(term.strip()) + r"(?!\w)"
    )
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(text, skills_path=None):
    """Return canonical skills found in resume text."""
    if not isinstance(text, str) or not text.strip():
        return []

    skills = load_skills(skills_path)
    found = []

    for canonical, aliases in skills.items():
        terms = [canonical, *aliases]

        if any(_contains_term(text, term) for term in terms):
            found.append(canonical)

    return found
