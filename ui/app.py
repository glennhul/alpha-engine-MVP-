import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models


st.set_page_config(page_title="alpha-engine", layout="wide")


@st.cache_data(ttl=60)
def load_latest(n=200):
with SessionLocal() as db:
df = pd.read_sql(db.query(models.Doc).order_by(models.Doc.published_at.desc()).limit(n).statement, db.bind)
return df


@st.cache_data(ttl=60)
def load_features():
with SessionLocal() as db:
df = pd.read_sql(db.query(models.Feature).statement, db.bind)
return df


st.title("alpha-engine (MVP)")


col1, col2 = st.columns([2,1])
with col1:
st.subheader("Latest docs")
docs = load_latest()
st.dataframe(docs[["published_at","title","tickers","sent_score"]])
with col2:
st.subheader("Features snapshot")
f = load_features()
if not f.empty:
latest = f.sort_values(["ticker","ts"]).groupby("ticker").tail(1)
latest = latest.sort_values("sent_mean", ascending=False)
st.dataframe(latest[["ticker","sent_mean","volume_msgs","novelty"]].reset_index(drop=True))
else:
st.write("No features yet")