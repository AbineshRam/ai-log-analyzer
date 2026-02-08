# AI Log Analyzer

FastAPI-based backend that ingests logs and uses AI (Sentence Transformers)
to classify them into error categories.

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite
- Sentence Transformers

## Run
pip install -r requirements.txt
uvicorn app.main:app --reload
