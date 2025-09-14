from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text, Float, Boolean
from app.db import Base
from datetime import datetime


class Doc(Base):
__tablename__ = "docs"
id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
source: Mapped[str] = mapped_column(String(64))
published_at: Mapped[datetime] = mapped_column(DateTime)
url: Mapped[str | None] = mapped_column(String(512), nullable=True)
title: Mapped[str] = mapped_column(String(512))
text: Mapped[str] = mapped_column(Text)
tickers: Mapped[str] = mapped_column(String(256), default="") # comma-separated
sent_pos: Mapped[float] = mapped_column(Float, default=0.0)
sent_neg: Mapped[float] = mapped_column(Float, default=0.0)
sent_neu: Mapped[float] = mapped_column(Float, default=0.0)
sent_score: Mapped[float] = mapped_column(Float, default=0.0)


class Feature(Base):
__tablename__ = "features"
id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
ts: Mapped[datetime] = mapped_column(DateTime)
ticker: Mapped[str] = mapped_column(String(16))
sent_mean: Mapped[float] = mapped_column(Float)
sent_std: Mapped[float] = mapped_column(Float)
pos_share: Mapped[float] = mapped_column(Float)
neg_share: Mapped[float] = mapped_column(Float)
volume_msgs: Mapped[int] = mapped_column(Integer)
novelty: Mapped[float] = mapped_column(Float)
event_earnings_up: Mapped[bool] = mapped_column(Boolean, default=False)