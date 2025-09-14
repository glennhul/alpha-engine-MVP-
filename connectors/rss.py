import feedparser
from datetime import datetime, timezone
from typing import Iterable
from connectors.base import Doc


DEFAULT_FEEDS = [
"https://www.wsj.com/feeds/rss/markets?mod=markets_directory",
"https://www.marketwatch.com/feeds/topstories",
"https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
"https://www.cnbc.com/id/100003114/device/rss/rss.html",
]


def parse_time(entry) -> datetime:
if hasattr(entry, "published_parsed") and entry.published_parsed:
return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
return datetime.now(tz=timezone.utc)


def fetch_once(feeds: list[str] | None = None) -> list[Doc]:
feeds = feeds or DEFAULT_FEEDS
docs: list[Doc] = []
for url in feeds:
fp = feedparser.parse(url)
for e in fp.entries:
text = (getattr(e, "summary", "") or "")
title = getattr(e, "title", "")
link = getattr(e, "link", None)
ts = parse_time(e)
docs.append(Doc(
source="rss",
published_at=ts,
title=title,
text=f"{title}\n\n{text}",
url=link,
meta={"feed": url}
))
return docs