import os, time
from sqlalchemy.orm import Session
from app.db import SessionLocal, init_db
from app import models
from nlp.pipeline import enrich_docs
from connectors.rss import fetch_once


POLL = int(os.getenv("RSS_POLL_SECONDS", "120"))


def save_docs(db: Session, records: list[dict]):
for r in records:
d = models.Doc(
source=r["source"],
published_at=r["published_at"],
url=r["url"],
title=r["title"],
text=r["text"],
tickers=",".join(r["tickers"]),
sent_pos=r["sent"]["pos"],
sent_neg=r["sent"]["neg"],
sent_neu=r["sent"]["neu"],
sent_score=r["sent"]["score"],
)
db.add(d)
db.commit()


if __name__ == "__main__":
init_db()
while True:
db = SessionLocal()
try:
raw = fetch_once()
enriched = enrich_docs(raw)
save_docs(db, enriched)
print(f"Ingested {len(enriched)} docs")
finally:
db.close()
time.sleep(POLL)