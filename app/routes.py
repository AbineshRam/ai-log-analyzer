from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Log, Analysis
from schemas import LogCreate, LogResponse, AnalysisResponse
from ai import analyze_log

router = APIRouter()


@router.post("/logs", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
def create_log(payload: LogCreate, db: Session = Depends(get_db)):
    log = Log(**payload.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.post("/logs/{log_id}/analyze", response_model=AnalysisResponse)
def analyze(log_id: int, db: Session = Depends(get_db)):
    log = db.query(Log).filter(Log.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    category, confidence = analyze_log(log.message)

    analysis = Analysis(
        log_id=log.id,
        category=category,
        confidence=confidence
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis
