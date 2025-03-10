from fastapi import HTTPException, status, APIRouter, Depends
from models import User, UserUpdate, UserPublic
from sqlmodel import Session, select
from database import engine
from auth import get_current_user
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Users"])
    
@router.put("/users")
def update_user(user: UserUpdate, current_user_id: int = Depends(get_current_user)) -> UserPublic:
    with Session(engine) as session:
        query = select(User).where(User.id == current_user_id)
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
    
@router.delete("/users")
def delete_user(current_user_id: int = Depends(get_current_user)):
    with Session(engine) as session:
        query = select(User).where(User.id == current_user_id)
        user_exists = session.exec(query).one_or_none()

        if user_exists is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        session.delete(user_exists)
        session.commit()
        return {"message": "User successfully deleted"}