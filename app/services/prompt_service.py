from app.schemas.prompt import PromptCreate
from app.schemas.prompt import PromptUpdate
from app.models.prompt import Prompt
from sqlalchemy.orm import Session
from app.repositories import prompt_repository
from app.exceptions.prompt import PromptNotFoundException

def create_prompt(prompt: PromptCreate, db: Session) -> Prompt:

    new_prompt =  Prompt(
        title=prompt.title,
        content=prompt.content,
        category=prompt.category,
    )

    return prompt_repository.create(new_prompt, db)



def get_prompts(db: Session):
    return prompt_repository.get_all(db)


def get_prompt(prompt_id: int, db: Session):
    prompt = prompt_repository.get_by_id(prompt_id, db)

    if prompt is None:
        raise PromptNotFoundException(prompt_id)

    return prompt


def update_partial_prompt(prompt_id: int, prompt_data: PromptUpdate, db: Session):
    prompt = prompt_repository.get_by_id(prompt_id, db)

    if prompt is None:
        raise PromptNotFoundException(f"Prompt with id {prompt_id} not found")

    update_data = prompt_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(prompt, field, value)

  
    return prompt_repository.update_patch(prompt, db)


def update_full_prompt(prompt_id: int, prompt_data: PromptCreate, db: Session):
    prompt = prompt_repository.get_by_id(prompt_id, db)

    if prompt is None:
        raise PromptNotFoundException(prompt_id)

    prompt.title = prompt_data.title
    prompt.content = prompt_data.content
    prompt.category = prompt_data.category

    return prompt_repository.update_prompt(prompt, db)

def delete_prompt(prompt_id: int, db: Session):
    prompt = prompt_repository.get_by_id(prompt_id, db)

    if prompt is None:
        raise PromptNotFoundException(prompt_id)

    return prompt_repository.delete_prompt(prompt, db)