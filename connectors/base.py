from dataclasses import dataclass
from datetime import datetime


@dataclass
class Doc:
source: str
published_at: datetime
title: str
text: str
url: str | None
meta: dict