from pydantic import BaseModel

class Post(BaseModel):
    id: int
    title: str
    description: str

class PostCreate(BaseModel):
    title: str
    description: str

class PostPublic(BaseModel):
    title: str
    description: str

class PostUpdate(PostCreate):
    pass
