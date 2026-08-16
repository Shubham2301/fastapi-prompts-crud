from fastapi import FastAPI, HTTPException, status, Depends
from app.schemas import PromptCreate, PromptResponse, PromptUpdate
from sqlalchemy import text, select

from app.db.database import engine, get_db

from sqlalchemy.orm import Session
from app.models.prompt import Prompt

app = FastAPI()

@app.get("/")
def root():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
    return {
        "message": "Prompt API is running",
        "database": result.scalar(),
    }


@app.post("/prompts", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    global next_id

    new_prompt =  Prompt(
        title=prompt.title,
        content=prompt.content,
        category=prompt.category,
    )


    db.add(new_prompt)
    db.commit()
    db.refresh(new_prompt)

    return new_prompt


@app.get("/prompts", response_model=list[PromptResponse], status_code=status.HTTP_200_OK)
def get_prompts(db: Session = Depends(get_db)):
    result = db.scalars(
        select(Prompt)
    )


    return result.all()


@app.get("/prompts/{prompt_id}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail = "Prompt not found!")

    return prompt



@app.patch("/prompts/{prompt_id}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
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

@app.put("prompts/{prompt_id}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
def update_full_prompt(prompt_id: int, prompt_data: PromptCreate, db: Session = Depends(get_db)):
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail = "Prompt not found!")

   
    prompt["title"] = prompt_data.title
    prompt["content"] = prompt_data.content
    prompt["category"] = prompt_data.category
    return prompt
        


@app.delete("/prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail = "Prompt not found!")

    db.delete(prompt)
    db.commit()

    return


