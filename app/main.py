from fastapi import FastAPI, Request, status
from app.routers.prompt import router as prompt_router
from app.db.database import engine
from sqlalchemy import text
from app.exceptions.prompt import PromptNotFoundException
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(prompt_router)

@app.exception_handler(PromptNotFoundException)
def prompt_not_found_exception_handler(request: Request, exc: PromptNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


@app.get("/")
def root():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
    return {
        "message": "Prompt API is running",
        "database": result.scalar(),
    }

