from sqlmodel import SQLModel, create_engine, Session
from app.config import database_url

connect_arg = {"check_same_thread": False} if "sqlite" in database_url else {}
engine = create_engine(database_url, connect_args=connect_arg)

def init_db():
    #create tables on startup
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
