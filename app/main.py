from fastapi import FastAPI, Request, status
from app.routers.prompt import router as prompt_router
from app.db.database import engine
from sqlalchemy import text
from app.exceptions.prompt import PromptNotFoundException, PromptAlreadyExistsException
from app.exceptions.validation import ValidationErrorException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.logging import setup_logging
from app.exceptions.error import error_body
import logging
from app.exceptions.llm import LlmUnavailableException


setup_logging()

app = FastAPI(title="Prompt Fast API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt_router, prefix="/api/v1")


logger = logging.getLogger(__name__)

@app.exception_handler(PromptNotFoundException)
def prompt_not_found_exception_handler(request: Request, exc: PromptNotFoundException):
    logger.warning("Prompt not found: id=%s", exc.prompt_id)

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_body("PROMPT_NOT_FOUND", str(exc)),
    )

@app.exception_handler(PromptAlreadyExistsException)
def prompt_already_exists_exception_handler(request: Request, exc: PromptAlreadyExistsException):
    logger.warning("Prompt already exists: title=%s", exc.prompt_title)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_body("PROMPT_ALREADY_EXISTS", str(exc)),
    )

@app.exception_handler(RequestValidationError)
def request_validation_error_handler(request: Request, exc: RequestValidationError):
    logger.info("Request validation failed")

    exc = ValidationErrorException(exc.errors())
    
    return JSONResponse(
        status_code=422,
        content=error_body("VALIDATION_ERROR", str(exc), details=exc.details),
    )


@app.exception_handler(LlmUnavailableException)
def llm_unavailable_exception_handler(request:Request, exc: LlmUnavailableException):
    logger.warning("Language model is unavailable")

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=error_body("SERVICE_UNAVAILABLE",str(exc)),
    )


@app.get("/")
def root():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
    return {
        "message": "Prompt API is running",
        "database": result.scalar(),
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
        return {
            "status": "OK",
        }
    except Exception as e:
        logger.exception("Health check failed: Database connection error")

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=error_body("SERVICE_UNAVAILABLE","Database unreachable"),
    )
