from fastapi import FastAPI, APIRouter
from database import create_db_and_tables, engine
from sqlmodel import Session, select
import posts

app = FastAPI()
create_db_and_tables()
app.include_router(posts.router)

@app.get("/")
def welcome():
    return {"message": "Welcome to social media API!"}
