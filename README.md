
# Automated Resume Analyzer

A Python-based project for extracting and organizing resume information, with planned natural language processing, machine learning, skill analysis, and job matching capabilities.

## Current Features

- Extract text from PDF resumes.
- Extract paragraphs and tables from DOCX resumes.
- Normalize extracted text.
- Identify common resume sections using heading rules.
- Process a resume through a modular pipeline.
- Run automated tests using pytest.

## Tech Stack

- Python
- pypdf
- python-docx
- pytest

## Project Structure

```text
automated-resume-analyzer/
├── src/
│   └── resume_analyzer/
│       ├── __init__.py
│       ├── extractor.py
│       ├── cleaner.py
│       ├── segmenter.py
│       └── pipeline.py
├── tests/
│   └── test_pipeline.py
├── samples/
│   └── sample_resume.txt
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Run

Process the included sample:

```powershell
python main.py
```

Process a PDF or DOCX resume:

```powershell
python main.py "path/to/resume.pdf"
python main.py "path/to/resume.docx"
```

### Run Tests

```powershell
python -m pytest -v
```

## Current Limitations

- Scanned PDFs require OCR.
- Section recognition relies on common headings.
- Complex resume layouts may affect extraction quality.
- Machine learning, skill matching, and job recommendations are planned features, not yet implemented.

## Roadmap

- **Day 1:** Repository, document extraction, text cleaning, section segmentation, and tests.
- **Day 2:** Resume feature extraction and initial NLP analysis.
- **Day 3:** Job-description matching and ranking.
- **Day 4:** Integration, evaluation, documentation, and final improvements.

## Privacy

Use synthetic or anonymized resumes for development. Do not commit real resumes, personal information, API keys, or other confidential data.

## License

License to be selected before public release.

# automated-resume-analyzer
An automated resume analyzer using Python, NLP and machine learning for resume parsing, skill extraction and job matching.

