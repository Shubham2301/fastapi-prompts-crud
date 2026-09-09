from sqlalchemy.orm import Session
from app.models.prompt import Prompt
from sqlalchemy import select, func
from typing import Optional

def create(prompt: Prompt, db: Session) -> Prompt:

    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    return prompt


def get_all(db: Session, limit: int, offset: int, category: Optional[str] = None, q: Optional[str] = None) -> tuple:
    query  = select(Prompt)

    if category is not None:
        query = query.where(Prompt.category == category)

    if q is not None:
        query = query.where(Prompt.title.ilike(f"%{q}%"))

    items = db.scalars(
        query.limit(limit).offset(offset)
    ).all()

    
    queryCount =  select(func.count()).select_from(query)
    total = db.scalar(queryCount)

    return items, total


def get_by_id(prompt_id: int, db: Session) -> Prompt:
   return db.get(Prompt, prompt_id)


def get_by_title(title: str, db: Session) -> Optional[Prompt]:
    return db.scalars(
        select(Prompt).where(Prompt.title == title)
    ).first()
  

def update_patch(prompt: Prompt, db: Session) -> Prompt:
    db.commit()
    db.refresh(prompt)

    return prompt


def update_prompt(prompt: Prompt, db: Session) -> Prompt:
    db.commit()
    db.refresh(prompt)

    return prompt


def delete_prompt(prompt: Prompt, db: Session):

    db.delete(prompt)
    db.commit()

    return
