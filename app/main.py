from fastapi import FastAPI
from app.db import init_db
from app.routes import router


app = FastAPI(title="alpha-engine API")
init_db()
app.include_router(router)