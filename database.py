from sqlmodel import create_engine, SQLModel

engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})

#check_same_thread makes sure that fastapi uses the same sqlite db for different threads

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)