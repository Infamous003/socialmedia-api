from fastapi import HTTPException, status, APIRouter, Depends
from models import Post, PostCreate, PostPublic, PostUpdate
from sqlmodel import Session, select, text
from database import engine
from auth import get_current_user

router = APIRouter(tags=["Posts"])

def create_posts():

    with Session(engine) as session:
        session.exec(text("PRAGMA foreign_keys=ON;"))
        posts = [
            Post(title="First Post", description="This is the first post description.", user_id=1),
            Post(title="Learning FastAPI", description="FastAPI makes API development fast and easy.", user_id=2),
            Post(title="Docker and Containers", description="Understanding how Docker works in DevOps.", user_id=1),
            Post(title="SQLModel Basics", description="An introduction to SQLModel and how it works.", user_id=3),
        ]

        session.add_all(posts)
        session.commit()
# create_posts()


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
def create_post(post: PostCreate, current_user_id: int = Depends(get_current_user)) -> PostPublic:
    with Session(engine) as session:
        print(post, "\n-----------------------")
        
        new_post = Post(**post.model_dump(), user_id=current_user_id)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post

@router.delete("/posts/{id}")
def delete_post(id: int, current_user_id: int = Depends(get_current_user)):
    with Session(engine) as session:
        query = select(Post).where(Post.user_id == current_user_id).where(Post.id == id)
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