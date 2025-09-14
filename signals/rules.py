import pandas as pd
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models
import click


WEIGHTS = {"sent_mean": 0.5, "novelty": 0.3, "volume_msgs": 0.2}


def rank_latest(db: Session, topn: int = 50) -> pd.DataFrame:
q = db.query(models.Feature)
df = pd.read_sql(q.statement, db.bind)
if df.empty:
return df
# pick the latest bucket per ticker
latest = df.sort_values(["ticker", "ts"]).groupby("ticker").tail(1)
z = latest.copy()
for c in ["sent_mean", "novelty", "volume_msgs"]:
z[c+"_z"] = (z[c] - z[c].mean()) / (z[c].std() + 1e-6)
z["score"] = (WEIGHTS["sent_mean"]*z["sent_mean_z"]
+ WEIGHTS["novelty"]*z["novelty_z"]
+ WEIGHTS["volume_msgs"]*z["volume_msgs_z"])
return z.sort_values("score", ascending=False).head(topn)


@click.command()
@click.option("--top", default=50, help="how many to print")
def cli(top):
with SessionLocal() as db:
out = rank_latest(db, top)
if out.empty:
print("No features yet. Run features/builder.py")
else:
print(out[["ticker","score","sent_mean","novelty","volume_msgs"]])


if __name__ == "__main__":
cli()