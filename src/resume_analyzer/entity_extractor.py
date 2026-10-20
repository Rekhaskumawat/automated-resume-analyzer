
import spacy


def load_nlp():
    """Load the English spaCy model with a useful error message."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError as exc:
        raise RuntimeError(
            "spaCy model 'en_core_web_sm' is missing. "
            "Install it with: "
            "python -m spacy download en_core_web_sm"
        ) from exc


_NLP = None


def extract_entities(text):
    """Extract common named entities from resume text."""
    result = {
        "persons": [],
        "organizations": [],
        "locations": [],
        "dates": [],
    }

    if not isinstance(text, str) or not text.strip():
        return result

    global _NLP
    if _NLP is None:
        _NLP = load_nlp()

    doc = _NLP(text)

    mapping = {
        "PERSON": "persons",
        "ORG": "organizations",
        "GPE": "locations",
        "LOC": "locations",
        "FAC": "locations",
        "DATE": "dates",
    }

    for ent in doc.ents:
        key = mapping.get(ent.label_)
        if key:
            value = ent.text.strip()
            if value and value not in result[key]:
                result[key].append(value)

    return result
