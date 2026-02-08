from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List
from fastapi import Query

from app.database import get_db
from app.models import Log, Analysis
from app.schemas import LogCreate, LogResponse, AnalysisResponse
from app.ai import analyze_log


router = APIRouter()

@router.get("/logs", response_model=List[LogResponse])
def list_logs(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * size
    logs = (
        db.query(Log)
        .order_by(Log.created_at.desc())
        .offset(offset)
        .limit(size)
        .all()
    )
    return logs



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
