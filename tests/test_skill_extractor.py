
from resume_analyzer.skill_extractor import extract_skills


def test_extract_skills():
    text = (
        "Experienced in Python, JavaScript, React.js, "
        "machine learning, and SQL."
    )

    result = extract_skills(text)

    assert "Python" in result
    assert "JavaScript" in result
    assert "React" in result
    assert "Machine Learning" in result
    assert "SQL" in result


def test_no_false_positive_for_c():
    result = extract_skills("I can communicate clearly with teams.")

    assert "C" not in result


def test_empty_skills():
    assert extract_skills("") == []
