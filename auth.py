from bcrypt import hashpw, gensalt, checkpw
import jwt
from fastapi import APIRouter, HTTPException, status, Depends
from models import UserCreate, User
from sqlmodel import Session, select
from database import engine
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


SECRET_KEY = "pls"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") # for setting up password flow dependency. Tells your app to expect a token in authorization header of inc req

def get_current_user(token: str = Depends(oauth2_scheme)):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["uid"]
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
  
@router.post("/register")
def register_user(user: UserCreate):
  with Session(engine) as session:
    query = select(User).where(User.username == user.username)
    user_exists = session.exec(query).first()

    if user_exists:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is already taken")
    
    user.password = hashpw(user.password.encode("utf-8"), gensalt())
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    return {"message": "User successfully created"}
  

@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends()):
  with Session(engine) as session:
    query = select(User).where(User.username == user.username)
    user_exists = session.exec(query).first()
    
    if not user_exists:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")

    if not checkpw(user.password.encode("utf-8"), user_exists.password):
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")
    
    expiration = datetime.utcnow() + timedelta(minutes=60)
    token = jwt.encode({"uid": user_exists.id, "sub": user_exists.username, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}