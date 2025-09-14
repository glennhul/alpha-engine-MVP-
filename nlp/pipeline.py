import os
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from connectors.base import Doc as RawDoc


HF_CACHE = os.getenv("HUGGINGFACE_CACHE", ".huggingface")
MODEL_NAME = "yiyanghkust/finbert-tone"


tok = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=HF_CACHE)
mdl = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, cache_dir=HF_CACHE)
mdl.eval()


TICK = pd.read_csv(os.path.join(os.path.dirname(__file__), "ticker_map.csv"))


ALIASES: list[tuple[str, str]] = [] # (alias_lower, ticker)
for _, r in TICK.iterrows():
for a in str(r.aliases).split("|"):
a = a.strip()
if a:
ALIASES.append((a.lower(), r.ticker))


@torch.inference_mode()
def _sentiment(batch: list[str]):
enc = tok(batch, padding=True, truncation=True, return_tensors="pt")
out = mdl(**enc).logits.softmax(-1).tolist()
res = []
for p in out:
neg, neu, pos = p
res.append({"neg": float(neg), "neu": float(neu), "pos": float(pos), "score": float(pos - neg)})
return res


def _tickers(text: str) -> list[str]:
t = text.lower()
hits = set()
for alias, ticker in ALIASES:
if alias in t:
hits.add(ticker)
return sorted(hits)


def enrich_docs(docs: list[RawDoc]):
texts = [d.text for d in docs]
sents = _sentiment(texts)
out = []
for d, s in zip(docs, sents):
out.append({
"source": d.source,
"published_at": d.published_at,
"url": d.url,
"title": d.title,
"text": d.text,
"tickers": _tickers(d.text),
"sent": s,
})
return out