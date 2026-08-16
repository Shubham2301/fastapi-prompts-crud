from fastapi import FastAPI, HTTPException, status
from app.schemas import PromptCreate, PromptResponse, PromptUpdate

app = FastAPI()

prompts = []
next_id = 1

@app.get("/")
def root():
    return {"message": "Welcome to Proompt CRUD Project"}


@app.post("/prompts", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
def create_prompt(prompt: PromptCreate):
    global next_id

    new_prompt = {
        "id": next_id,
        "title": prompt.title,
        "content": prompt.content,
        "category": prompt.category,
    }

    prompts.append(new_prompt)
    next_id += 1

    return new_prompt


@app.get("/prompts", response_model=list[PromptResponse], status_code=status.HTTP_200_OK)
def get_prompts():
    return prompts


@app.get("/prompts/{prompt_id}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
def get_prompt(prompt_id: int):
    for prompt in prompts:
        if prompt["id"] == prompt_id:
            return prompt
    
    raise HTTPException(status_code=404, detail = "Prompt not found!")


@app.patch("/prompts/{prompt_id}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
def update_partial_prompt(prompt_id: int, prompt_data: PromptUpdate):
    for prompt in prompts:
        if prompt["id"] == prompt_id:

            update_data = prompt_data.model_dump(exclude_unset=True)

            prompt.update(update_data)
            return prompt
        
    raise HTTPException(status_code=404, detail="Prompt not found!") 

@app.put("prompts/{prompt_id}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
def update_full_prompt(prompt_id: int, prompt_data: PromptCreate):
    for prompt in prompts:
        if prompt["id"] == prompt_id:
            prompt["title"] = prompt_data.title
            prompt["content"] = prompt_data.content
            prompt["category"] = prompt_data.category
            return prompt
        
    raise HTTPException(status_code=404, detail="Prompt not found!")


@app.delete("/prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prompt(prompt_id: int):
    for index, prompt in enumerate(prompts):
        if prompt["id"] == prompt_id:
            prompts.pop(index)

            return
        
    raise HTTPException(status_code=404, detail="Prompt not found!")


