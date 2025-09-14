# alpha-engine (MVP)


An open-source, news+social alpha engine (MVP) that:
- Ingests RSS news (you can add more sources later)
- Maps text to tickers and scores sentiment (FinBERT)
- Aggregates features per ticker & time window
- Ranks long/short candidates with a simple rule
- Backtests on daily bars
- Shows a basic Streamlit dashboard


> ⚠️ Educational use only. This is **not investment advice**. Use at your own risk.


## Quickstart (no Docker)
```bash
# 1) Create venv and install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt


# 2) Set env
cp .env.example .env
# edit .env to set DATABASE_URL, HUGGINGFACE_CACHE, etc.


# 3) Start Postgres (if you have it locally) or use Docker (see below)


# 4) Initialize DB tables
python -m app.db --init


# 5) Run the ingestor (RSS)
python connectors/ingest.py


# 6) Build features (per 15m window by default)
python features/builder.py


# 7) Rank signals
python -c "from signals.rules import cli; cli()"


# 8) Run the dashboard
streamlit run ui/app.py