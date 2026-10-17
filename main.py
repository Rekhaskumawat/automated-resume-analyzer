
import argparse
import json
from pathlib import Path

from src.resume_analyzer import process_resume


def main():
    parser = argparse.ArgumentParser(
        description="Extract and organize resume text."
    )

    parser.add_argument(
        "resume",
        nargs="?",
        default="samples/sample_resume.txt",
        help="Path to a PDF or DOCX resume.",
    )

    args = parser.parse_args()
    path = Path(args.resume)

    # Text samples are useful for testing segmentation directly.
    if path.suffix.lower() == ".txt":
        from src.resume_analyzer.cleaner import clean_text
        from src.resume_analyzer.segmenter import segment_sections

        text = clean_text(path.read_text(encoding="utf-8"))
        result = {
            "file_name": path.name,
            "cleaned_text": text,
            "sections": segment_sections(text),
        }
    else:
        result = process_resume(path)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
