
from resume_analyzer.contact_extractor import extract_contacts


def test_extract_contacts():
    text = (
        "Email: candidate@example.com\n"
        "Phone: +91 98765 43210\n"
        "Portfolio: https://example.com"
    )

    result = extract_contacts(text)

    assert "candidate@example.com" in result["emails"]
    assert "https://example.com" in result["urls"]
    assert any("98765" in phone for phone in result["phones"])


def test_missing_contacts():
    result = extract_contacts("No contact information here.")

    assert result == {"emails": [], "phones": [], "urls": []}


def test_empty_input():
    assert extract_contacts("") == {
        "emails": [], "phones": [], "urls": []
    }
