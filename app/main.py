from fastapi import FastAPI, HTTPException
from app.schemas import PromptCreate, PromptResponse

app = FastAPI()

prompts = []
next_id = 1

@app.get("/")
def root():
    return {"message": "Welcome to Proompt CRUD Project"}


@app.post("/prompt")
def create_prompt(prompt: PromptCreate, response_model=PromptResponse):
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


@app.get("/prompts")
def get_prompts(response_model=PromptResponse):
    return prompts


@app.get("/prompts/{prompt_id}")
def get_prompt(prompt_id: int,response_model=PromptResponse):
    for prompt in prompts:
        if prompt["id"] == prompt_id:
            return prompt
    
    raise HTTPException(status_code=404, detail = "Prompt not found!")


@app.put("/prompts/{prompt_id}")
def update_prompt(prompt_id: int, prompt_data: PromptCreate, response_model=PromptResponse):
    for prompt in prompts:
        if prompt["id"] == prompt_id:
            prompt["title"] = prompt_data.title;
            prompt["content"] = prompt_data.content;
            prompt["category"] = prompt_data.category;
            return prompt
        
    raise HTTPException(status_code=404, detail="Prompt not found!")


@app.delete("/prompts/{prompt_id}")
def delete_prompt(prompt_id: int):
    for index, prompt in enumerate(prompts):
        if prompt["id"] == prompt_id:
            prompts.pop(index)

            return {"message": "Prompt deleted successfully!"}
        
    raise HTTPException(status_code=404, detail="Prompt not found!")


