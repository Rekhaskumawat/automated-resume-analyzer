
from resume_analyzer.entity_extractor import extract_entities


def test_extract_entities():
    text = (
        "Rahul Sharma worked at Microsoft in Hyderabad "
        "from January 2023 to March 2025."
    )

    result = extract_entities(text)

    assert "Rahul Sharma" in result["persons"]
    assert any(
        "Microsoft" in org for org in result["organizations"]
    )
    assert any(
        "Hyderabad" in location
        for location in result["locations"]
    )
    assert result["dates"]


def test_empty_entities():
    result = extract_entities("")

    assert result == {
        "persons": [],
        "organizations": [],
        "locations": [],
        "dates": [],
    }
