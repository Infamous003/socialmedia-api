from fastapi import FastAPI, HTTPException, status
from models import Post
from database import create_db_and_tables

app = FastAPI()
create_db_and_tables()

@app.get("/")
def welcome():
    return {"message": "Welcome to social media API!"}

POSTS = [
    {"id": 1, "title": "Shutter Island | Movie breakdown", "description": "Shutter Island is a psychological thriller by none other than the great producer Christopher Nolan..."},
    {"id": 2, "title": "Batman 2022 Review", "description": "After over a decade of waiting, we have finally come back to Gotham..."},
    {"id": 3, "title": "A Separation", "description": "The Iranian Oscar winning movie is about a family which is going through divorce but something unexpected happens..."},
]

@app.get("/posts")
def get_posts():
    return POSTS

@app.get("/posts/{id}")
def get_posts(id: int):
    post_exists = [post for post in POSTS if post["id"] == id]
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post_exists

@app.post("/posts")
def create_post(post: Post):
    POSTS.append(post)
    return {"message": "Post created successfully"}
