from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.db.database import get_db
from app.schemas.prompt import PromptCreate, PromptUpdate
from app.models.prompt import Prompt
from sqlalchemy import select

def create_prompt(new_prompt: PromptCreate, db: Session = Depends(get_db)) -> Prompt:

    db.add(new_prompt)
    db.commit()
    db.refresh(new_prompt)

    return new_prompt


def get_prompts(db: Session = Depends(get_db)):
    result = db.scalars(
        select(Prompt)
    )

    return result.all()


def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail = "Prompt not found!")

    return prompt


def update_partial_prompt(prompt_id: int, prompt_data: PromptUpdate, db: Session = Depends(get_db)):
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail = "Prompt not found!")

    update_data = prompt_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(prompt, field, value)

    db.commit()
    db.refresh(prompt)

    return prompt


def update_full_prompt(prompt_id: int, prompt_data: PromptCreate, db: Session = Depends(get_db)):
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail = "Prompt not found!")

   
    prompt.title = prompt_data.title
    prompt.content = prompt_data.content
    prompt.category = prompt_data.category
    return prompt


def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail = "Prompt not found!")

    db.delete(prompt)
    db.commit()

    return
