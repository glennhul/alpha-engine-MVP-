import argparse
import os
import pandas as pd
import yfinance as yf


PRICES_DIR = os.path.join(os.path.dirname(__file__), "prices")
os.makedirs(PRICES_DIR, exist_ok=True)


def main(start: str, end: str, tickers: list[str] | None):
if not tickers:
# read from ticker_map.csv
tdf = pd.read_csv(os.path.join(os.path.dirname(__file__), "../nlp/ticker_map.csv"))
tickers = sorted(set(tdf["ticker"].tolist()))
data = yf.download(tickers, start=start, end=end, progress=False)["Adj Close"]
data.to_csv(os.path.join(PRICES_DIR, "daily.csv"))
print(f"Saved {data.shape} to prices/daily.csv")


if __name__ == "__main__":
p = argparse.ArgumentParser()
p.add_argument("--start", required=True)
p.add_argument("--end", required=True)
p.add_argument("--tickers", nargs="*")
args = p.parse_args()
main(args.start, args.end, args.tickers)