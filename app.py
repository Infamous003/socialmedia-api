from fastapi import FastAPI
from database import create_db_and_tables
import posts

app = FastAPI()
create_db_and_tables()
app.include_router(posts.router)

@app.get("/")
def welcome():
    return {"message": "Welcome to social media API!"}
