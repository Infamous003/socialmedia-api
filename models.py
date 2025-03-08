from pydantic import BaseModel
from sqlmodel import SQLModel, Field, String

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(String() ,nullable=False, min_length=5)
    description: str = Field(String(), min_length=10)

class PostCreate(BaseModel):
    title: str
    description: str

class PostPublic(BaseModel):
    title: str
    description: str

class PostUpdate(PostCreate):
    title: str | None = None
    description: str | None = None

