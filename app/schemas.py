from pydantic import BaseModel

class PromptCreate(BaseModel):
    title: str
    content: str
    category:str


class PromptResponse(BaseModel):
    id: int
    title: str
    content: str
    category:str