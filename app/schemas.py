from pydantic import BaseModel
from typing import Optional

class PromptCreate(BaseModel):
    title: str
    content: str
    category:str


class PromptResponse(BaseModel):
    id: int
    title: str
    content: str
    category:str

class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None