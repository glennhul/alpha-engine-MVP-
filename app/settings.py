from pydantic import BaseModel
import os


class Settings(BaseModel):
database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://alpha:alpha@localhost:5432/alpha")
api_host: str = os.getenv("API_HOST", "0.0.0.0")
api_port: int = int(os.getenv("API_PORT", 8000))


settings = Settings()