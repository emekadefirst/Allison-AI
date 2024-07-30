from datetime import datetime
from sqlmodel import SQLModel, Field
from database import create_db

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author_name: str
    description: str 
    categories: str
    release_date: str
    file: str
    cover_image: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BookSummary(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    text_summary: str
    audio_summary: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def __str__(self):
        return f"Summary for book id: {self.book_id}"

create_db()