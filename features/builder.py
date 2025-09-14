from datetime import datetime
def build_once(db: Session):
# Load last 24h of docs
q = db.query(models.Doc)
rows = pd.read_sql(q.statement, db.bind)
if rows.empty:
return 0
rows["bucket"] = rows["published_at"].dt.floor(f"{WINDOW_MIN}min")
feat = []
for (bucket, ticker), grp in (
rows.explode("tickers")
.assign(tickers=rows["tickers"].str.split(","))
.explode("tickers")
.dropna(subset=["tickers"])
.groupby(["bucket", "tickers"])):
s = grp["sent_score"].astype(float)
pos = grp["sent_pos"].astype(float)
neg = grp["sent_neg"].astype(float)
total = len(grp)
feat.append({
"ts": bucket,
"ticker": ticker,
"sent_mean": s.mean(),
"sent_std": s.std(ddof=0) if total > 1 else 0.0,
"pos_share": float((pos > neg).sum()) / total,
"neg_share": float((neg > pos).sum()) / total,
"volume_msgs": int(total),
"novelty": float(1.0 / (1 + total)), # naive novelty proxy
"event_earnings_up": False,
})
if not feat:
return 0
df = pd.DataFrame(feat)
# upsert
for _, r in df.iterrows():
db.merge(models.Feature(
ts=r.ts,
ticker=r.ticker,
sent_mean=r.sent_mean,
sent_std=r.sent_std,
pos_share=r.pos_share,
neg_share=r.neg_share,
volume_msgs=r.volume_msgs,
novelty=r.novelty,
event_earnings_up=r.event_earnings_up,
))
db.commit()
return len(df)


if __name__ == "__main__":
with SessionLocal() as db:
n = build_once(db)
print(f"Built {n} feature rows")