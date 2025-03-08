from fastapi import HTTPException, status, APIRouter
from models import Post, PostCreate, PostPublic, PostUpdate
from sqlmodel import Session, select
from database import engine

router = APIRouter(tags=["Posts"])

@router.get("/posts")
def get_posts():
    with Session(engine) as session:
        query = select(Post)
        posts = session.exec(query).all()
        return posts

@router.get("/posts/{id}")
def get_posts(id: int) -> PostPublic:
    with Session(engine) as session:
        query = select(Post).where(Post.id == id)
        post_exists = session.exec(query).one_or_none()
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post_exists

@router.post("/posts")
def create_post(post: PostCreate) -> PostPublic:
    with Session(engine) as session:
        new_post = Post(**post.model_dump())
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post

@router.delete("/posts/{id}")
def delete_post(id: int):
    with Session(engine) as session:
        query = select(Post).where(Post.id == id)
        post_exists = session.exec(query).one_or_none()

        if post_exists is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        session.delete(post_exists)
        session.commit()
        return {"message": "Post successfully deleted"}
    
@router.put("/posts/{id}")
def update_post(id: int, post: PostUpdate):
    with Session(engine) as session:
        query = select(Post).where(Post.id == id)
        post_exists = session.exec(query).one_or_none()

    if post_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.title:
        post_exists.title = post.title
    if post.description:
        post_exists.description = post.description

    session.add(post_exists)
    session.commit()
    session.refresh(post_exists)
    return post_exists