from fastapi import FastAPI
from app.routers.prompt import router as prompt_router
from app.db.database import engine
from sqlalchemy import text

app = FastAPI()

app.include_router(prompt_router)


@app.get("/")
def root():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
    return {
        "message": "Prompt API is running",
        "database": result.scalar(),
    }

