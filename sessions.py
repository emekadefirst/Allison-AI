from sqlmodel import Session, select
from models import Book, BookSummary
from database import engine

def create_book(title, author_name, description, categories, release_date, file, cover_image):
    with Session(engine) as session:
        data = Book(
            title=title,
            author_name=author_name,
            description=description,
            categories=categories,
            release_date=release_date,  
            file=file,
            cover_image=cover_image
        )
        session.add(data)
        session.commit()
        return "Book created"
def all_books():
    with Session(engine) as session:
        statement = select(Book)
        results = session.exec(statement).all()
        return results

def get_book_by_id(book_id):
    with Session(engine) as session:
        statement = select(Book).where(Book.id == book_id)
        result = session.exec(statement).one_or_none()
        return result

def update_book(book_id, title=None, author_name=None, description=None, categories=None, release_date=None, file=None, cover_image=None):
    with Session(engine) as session:
        statement = select(Book).where(Book.id == book_id)
        book = session.exec(statement).one_or_none()
        if book:
            if title:
                book.title = title
            if author_name:
                book.author_name = author_name
            if description:
                book.description = description
            if categories:
                book.categories = categories
            if release_date:
                book.release_date = release_date
            if file:
                book.file = file
            if cover_image:
                book.cover_image = cover_image
            session.add(book)
            session.commit()
            return f"Book with id {book_id} has been successfully updated"
        return f"No book found with id: {book_id}"

def delete_book(book_id):
    with Session(engine) as session:
        book = session.exec(select(Book).where(Book.id == book_id)).one_or_none()
        if book:
            session.delete(book)
            session.commit()
            return f'Book with id {book_id} has been successfully deleted'
        return f"No book found with id: {book_id}"

def search_book(query_input: str):
    with Session(engine) as session:
        statement = select(Book).where(
            (Book.title.contains(query_input)) |
            (Book.author_name.contains(query_input)) |
            (Book.description.contains(query_input))
        )
        results = session.exec(statement).all()
        return results

"""BookSummary sessions to perform CREATE and READ operations"""
def create_book_summary(book_id, text_summary, audio_summary):
    with Session(engine) as session:
        data = BookSummary(book_id=book_id, text_summary=text_summary, audio_summary=audio_summary)
        session.add(data)
        session.commit()
        return "Book summary created"

def all_book_summaries():
    with Session(engine) as session:
        statement = select(BookSummary)
        results = session.exec(statement).all()
        return results

def get_book_summary_by_id(summary_id):
    with Session(engine) as session:
        statement = select(BookSummary).where(BookSummary.id == summary_id)
        result = session.exec(statement).one_or_none()
        return result
