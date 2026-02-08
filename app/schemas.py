from datetime import datetime
from pydantic import BaseModel


class LogCreate(BaseModel):
    level: str
    source: str
    message: str


class LogResponse(LogCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisResponse(BaseModel):
    id: int
    log_id: int
    category: str
    confidence: int
    created_at: datetime

    class Config:
        from_attributes = True
