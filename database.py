import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

def create_db():
    # db_url = os.environ.get('postgresql_ex_url')
    db_url = 'postgresql://alison_40fc_user:2kJzZNhtr8HJMXsLPojvWAymkOhcL6TZ@dpg-cqkrr10gph6c738k8du0-a.oregon-postgres.render.com/alison_40fc'
    if db_url is None:
        raise ValueError("PostgreSQL URL not found in environment variables")
    print(f"Database URL: {db_url}")  # Debugging print
    engine = create_engine(db_url, echo=True)
    SQLModel.metadata.create_all(engine)
    return engine

engine = create_db()
