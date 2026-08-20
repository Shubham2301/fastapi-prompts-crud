from sqlalchemy.orm import Session
from app.models.prompt import Prompt
from sqlalchemy import select


def create(prompt: Prompt, db: Session) -> Prompt:

    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    return prompt


def get_all(db: Session) -> list[Prompt]:
    result = db.scalars(
        select(Prompt)
    )

    return result.all()


def get_by_id(prompt_id: int, db: Session) -> Prompt:
   return db.get(Prompt, prompt_id)
  


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
