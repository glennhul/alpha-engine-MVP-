from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models


router = APIRouter()


def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()


@router.get("/docs/latest")
def latest_docs(limit: int = 50, db: Session = Depends(get_db)):
q = db.query(models.Doc).order_by(models.Doc.published_at.desc()).limit(limit)
out = []
for d in q.all():
out.append({
"id": d.id,
"source": d.source,
"published_at": d.published_at,
"url": d.url,
"title": d.title,
"tickers": d.tickers.split(",") if d.tickers else [],
"sent_score": d.sent_score,
})
return out