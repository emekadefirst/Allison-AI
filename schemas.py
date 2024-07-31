from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author_name: str
    description: str
    categories: str

class BookUpdate(BaseModel):
    title: Optional[str]
    author_name: Optional[str]
    description: Optional[str]
    categories: Optional[str]
    release_date: Optional[str]

class BookSummaryCreate(BaseModel):
    book_id: int
    text_summary: str
    audio_summary: Optional[str]
    


class BookQuery(BaseModel):
    query: str
