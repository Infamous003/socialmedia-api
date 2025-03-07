from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class Post(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field()

class PostCreate(BaseModel):
    title: str
    description: str

class PostPublic(BaseModel):
    title: str
    description: str

class PostUpdate(PostCreate):
    pass
