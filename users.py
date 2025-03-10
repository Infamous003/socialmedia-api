from fastapi import HTTPException, status, APIRouter
from models import User, UserPublic, UserCreate, UserUpdate
from sqlmodel import Session, select
from database import engine
from bcrypt import hashpw, gensalt

router = APIRouter(tags=["Users"])
    
@router.put("/users/{id}")
def update_user(id: int, user: UserUpdate):
    with Session(engine) as session:
        query = select(User).where(User.id == id)
        user_exists = session.exec(query).one_or_none()

        if user_exists is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user.username:
            user_exists.username = user.username
        if user.password:
            user_exists.password = user.password
        session.add(user_exists)
        session.commit()
        session.refresh(user_exists)
        return user_exists
    
@router.delete("/users/{id}")
def delete_user(id: int):
    with Session(engine) as session:
        query = select(User).where(User.id == id)
        user_exists = session.exec(query).one_or_none()

        if user_exists is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        session.delete(user_exists)
        session.commit()
        return {"message": "User successfully deleted"}