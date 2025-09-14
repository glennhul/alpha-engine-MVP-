import argparse
PRICES_CSV = os.path.join(os.path.dirname(__file__), "prices/daily.csv")


def run_bt(start: str, end: str, long_n: int, short_n: int):
with SessionLocal() as db:
feats = pd.read_sql(db.query(models.Feature).statement, db.bind)
prices = pd.read_csv(PRICES_CSV, index_col=0, parse_dates=True)
prices = prices.loc[start:end]


# rank per day using latest features up to that day
feats = feats.sort_values("ts")
dates = sorted(set(prices.index.date))
equity = []
val = 1.0
for d in dates:
day = pd.Timestamp(d)
fs = feats[feats["ts"] <= day]
if fs.empty:
equity.append((day, val))
continue
latest = fs.sort_values(["ticker","ts"]).groupby("ticker").tail(1)
# zscore & score
z = latest.copy()
for c in ["sent_mean","novelty","volume_msgs"]:
z[c+"_z"] = (z[c]-z[c].mean())/(z[c].std()+1e-6)
z["score"] = 0.5*z["sent_mean_z"] + 0.3*z["novelty_z"] + 0.2*z["volume_msgs_z"]
longs = z.sort_values("score", ascending=False).head(long_n)["ticker"].tolist()
shorts = z.sort_values("score", ascending=True).head(short_n)["ticker"].tolist()
# compute next-day returns
next_day = day + pd.Timedelta(days=1)
if next_day not in prices.index:
equity.append((day, val))
continue
ret_long = prices.loc[next_day, longs].pct_change().iloc[-1].mean() if longs else 0
ret_short = -prices.loc[next_day, shorts].pct_change().iloc[-1].mean() if shorts else 0
ret = 0.5*ret_long + 0.5*ret_short
val *= (1 + ret)
equity.append((next_day, val))
eq = pd.DataFrame(equity, columns=["date","equity"]).set_index("date")
return eq


if __name__ == "__main__":
p = argparse.ArgumentParser()
p.add_argument("--start", required=True)
p.add_argument("--end", required=True)
p.add_argument("--long", type=int, default=10)
p.add_argument("--short", type=int, default=10)
args = p.parse_args()
eq = run_bt(args.start, args.end, args.long, args.short)
stats = {
"CAGR": (eq.iloc[-1,0])**(252/len(eq)) - 1 if len(eq)>0 else 0,
"MaxDD": (eq/eq.cummax() - 1).min().values[0] if len(eq)>0 else 0,
}
print(eq.tail())
print(stats)