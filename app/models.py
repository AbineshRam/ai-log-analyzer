from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)
    source = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)
    confidence = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
