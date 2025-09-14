from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import argparse
from app.settings import settings


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
pass


from app.models import * # noqa


def init_db():
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
parser = argparse.ArgumentParser()
parser.add_argument("--init", action="store_true")
args = parser.parse_args()
if args.init:
init_db()
with engine.connect() as conn:
conn.execute(text("select 1"))
print("DB initialized")