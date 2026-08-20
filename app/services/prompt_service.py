from app.schemas.prompt import PromptCreate
from app.schemas.prompt import PromptUpdate
from app.models.prompt import Prompt
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.repositories.prompt_repository import create_prompt as create_prompt_repository
from app.repositories.prompt_repository import get_prompts as get_prompts_repository
from app.repositories.prompt_repository import get_prompt as get_prompt_repository
from app.repositories.prompt_repository import update_partial_prompt as update_partial_prompt_repository
from app.repositories.prompt_repository import update_full_prompt as update_full_prompt_repository
from app.repositories.prompt_repository import delete_prompt as delete_prompt_repository

def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)) -> Prompt:

    new_prompt =  Prompt(
        title=prompt.title,
        content=prompt.content,
        category=prompt.category,
    )

    return create_prompt_repository(new_prompt, db)



def get_prompts(db: Session = Depends(get_db)):
    return get_prompts_repository(db)


def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    return get_prompt_repository(prompt_id, db)


def update_partial_prompt(prompt_id: int, prompt_data: PromptUpdate, db: Session = Depends(get_db)):
    return update_partial_prompt_repository(prompt_id, prompt_data, db)


def update_full_prompt(prompt_id: int, prompt_data: PromptCreate, db: Session = Depends(get_db)):
    return update_full_prompt_repository(prompt_id, prompt_data, db)

def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    return delete_prompt_repository(prompt_id, db)