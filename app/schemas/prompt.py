from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PromptCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    content: str = Field(min_length=30, max_length=1000)
    category:str = Field(min_length=3, max_length=255)


class PromptResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    category:str

class PromptUpdate(BaseModel):
    title: Optional[str] = Field(default=None,min_length=3, max_length=255)
    content: Optional[str] = Field(default=None, min_length=30, max_length=1000)
    category: Optional[str] = Field(default=None, min_length=3, max_length=255)


class PromptListResponse(BaseModel):
    items: list[PromptResponse]
    total: int
    limit: int
    offset: int