import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

def create_db():
    try:
        db_url = os.environ.get('postresql_ex_url')
        if db_url is None:
            raise ValueError("PostgreSQL URL not found in environment variables")
        engine = create_engine(db_url, echo=True)
    except (SQLAlchemyError, ValueError) as e:
        print(f"Failed to connect to PostgreSQL: {str(e)}")
        print("Falling back to SQLite")
        sqlite_file_name = "alison_ai_data.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        engine = create_engine(sqlite_url, echo=True)
    
    SQLModel.metadata.create_all(engine)
    return engine

engine = create_db()