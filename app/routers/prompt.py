from fastapi import APIRouter, status, Depends, Query
from app.schemas.prompt import PromptCreate, PromptResponse, PromptUpdate, PromptListResponse
from typing import Optional, Literal

from app.db.database import  get_db

from sqlalchemy.orm import Session
from app.services.prompt_service import create_prompt as create_prompt_service
from app.services.prompt_service import get_prompts as get_prompts_service
from app.services.prompt_service import get_prompt as get_prompt_service
from app.services.prompt_service import update_partial_prompt as update_partial_prompt_service
from app.services.prompt_service import update_full_prompt as update_full_prompt_service
from app.services.prompt_service import delete_prompt as delete_prompt_service




router = APIRouter(
    prefix="/prompts",
    tags=["Prompts"],
)



@router.post("/", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    return create_prompt_service(prompt, db)


@router.get("/", response_model=PromptListResponse, status_code=status.HTTP_200_OK)
def get_prompts(
    db: Session = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    category: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None, min_length=1),
    sort_by: Literal["id", "title", "category"] = Query(default="id"),
    sort_order: Literal["asc", "desc"] = Query(default="asc")
):
    items, total = get_prompts_service(db, limit, offset, category, q, sort_by, sort_order)

    return PromptListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{prompt_id}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    return get_prompt_service(prompt_id, db)



@router.patch("/{prompt_id}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
def update_partial_prompt(prompt_id: int, prompt_data: PromptUpdate, db: Session = Depends(get_db)):
    return update_partial_prompt_service(prompt_id, prompt_data, db)

@router.put("/{prompt_id}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
def update_full_prompt(prompt_id: int, prompt_data: PromptCreate, db: Session = Depends(get_db)):
    return update_full_prompt_service(prompt_id, prompt_data, db)
        


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    return delete_prompt_service(prompt_id, db)