
import argparse
import json
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.parser import ResumeParser


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Automated Resume Analyzer",
    description="Extract contact information, entities, skills, and sections from resumes.",
    version="1.0.0",
)

resume_parser = ResumeParser()
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@app.get("/")
def home():
    return {
        "message": "Automated Resume Analyzer API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Accept a PDF or DOCX resume and return extracted information."""
    filename = Path(file.filename or "").name

    if not filename:
        raise HTTPException(status_code=400, detail="A filename is required.")

    extension = Path(filename).suffix.lower()

    if extension not in {".pdf", ".docx"}:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type. Upload a PDF or DOCX file.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum upload size is 10 MB.",
        )

    temp_path = None

    try:
        with NamedTemporaryFile(
            suffix=extension,
            delete=False,
        ) as temp_file:
            temp_file.write(content)
            temp_path = Path(temp_file.name)

        try:
            result = resume_parser.parsefile(temp_path)
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:
            logger.warning("Resume parsing failed: %s", exc)
            raise HTTPException(
                status_code=422,
                detail="Unable to parse this resume. Check that the file is valid.",
            ) from exc

        # Return the uploaded filename instead of the temporary filename.
        result["file_name"] = filename
        return result

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        await file.close()


def main():
    """Command-line interface for parsing resumes."""
    cli_parser = argparse.ArgumentParser(
        description="Parse a PDF or DOCX resume into structured JSON."
    )

    cli_parser.add_argument(
        "resume",
        help="Path to a PDF or DOCX resume.",
    )

    args = cli_parser.parse_args()

    try:
        result = resume_parser.parsefile(Path(args.resume))
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ValueError, FileNotFoundError) as exc:
        cli_parser.error(str(exc))


if __name__ == "__main__":
    main()
