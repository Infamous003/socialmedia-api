from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, String, Relationship, DateTime
from datetime import datetime

# USER Models

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(String(32), nullable=False, unique=True, index=True)
    email: EmailStr = Field(String(128), nullable=False)
    password: str = Field(String(128), nullable=False)
    post: list["Post"] = Relationship(back_populates="user", cascade_delete=True)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: int
    username: str

class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None

class UserLogin(BaseModel):
    username: str | None = None
    password: str | None = None

# Post models

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(String() ,nullable=False, min_length=5)
    description: str = Field(String(), min_length=10)
    published_at: datetime = Field(default_factory=datetime.now)
    user_id: int = Field(nullable=False, foreign_key="user.id", ondelete="CASCADE")
    user: User = Relationship(back_populates="post")

class PostCreate(BaseModel):
    title: str
    description: str

class PostPublic(BaseModel):
    title: str
    description: str

class PostUpdate(PostCreate):
    title: str | None = None
    description: str | None = None