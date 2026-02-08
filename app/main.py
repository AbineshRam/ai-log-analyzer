from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routes import router


app = FastAPI(
    title="AI Log Analyzer",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "UP"}
