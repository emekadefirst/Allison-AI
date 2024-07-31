import os
import shutil
from summary import model
from typing import Optional
from schemas import BookUpdate, BookQuery
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from sessions import create_book, all_books, get_book_by_id, update_book, delete_book, search_book


app = FastAPI(
    title="Allison AI",
    description="API For Allison AI",
    version="0.1.0"
)

app.include_router(model, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOOK_IMAGE_DIRECTORY = "./book_image/"
if not os.path.exists(BOOK_IMAGE_DIRECTORY):
    os.makedirs(BOOK_IMAGE_DIRECTORY)
    
AUDIO_SUMMARY_DIR = "./book_audio_summary/"
if not os.path.exists(AUDIO_SUMMARY_DIR):
    os.makedirs(AUDIO_SUMMARY_DIR)


BOOK_FILE_DIRECTORY = "./book_file/"
if not os.path.exists(BOOK_FILE_DIRECTORY):
    os.makedirs(BOOK_FILE_DIRECTORY)

@app.post("/books/")
async def create_book_endpoint(
    title: str = Form(...),
    author_name: str = Form(...),
    description: str = Form(...),
    categories: str = Form(...),
    release_date: str = Form(...),
    file: Optional[UploadFile] = File(None), 
    cover_image: Optional[UploadFile] = File(None)  
):
    file_path = None
    if file:
        file_path = os.path.join(BOOK_FILE_DIRECTORY, file.filename)
        try:
            with open(file_path, "wb") as book_file:
                shutil.copyfileobj(file.file, book_file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File error: {str(e)}")

    cover_image_path = None
    if cover_image:
        cover_image_path = os.path.join(BOOK_IMAGE_DIRECTORY, cover_image.filename)
        try:
            with open(cover_image_path, "wb") as image_file:
                shutil.copyfileobj(cover_image.file, image_file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image error: {str(e)}")
    
    return create_book(
        title=title,
        author_name=author_name,
        description=description,
        categories=categories,
        release_date=release_date,
        file=file_path,
        cover_image=cover_image_path
    )

@app.get("/books/")
def all_books_endpoint():
    return all_books()

@app.get("/books/{book_id}")
def get_book_by_id_endpoint(book_id: int):
    book = get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}")
async def update_book_endpoint(
    book_id: int,
    title: Optional[str] = Form(None),
    author_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    categories: Optional[str] = Form(None),
    release_date: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),  # File upload for the book
    cover_image: Optional[UploadFile] = File(None)  # File upload for the cover image
):
    file_path = None
    if file:
        file_path = os.path.join(BOOK_FILE_DIRECTORY, file.filename)
        with open(file_path, "wb") as book_file:
            shutil.copyfileobj(file.file, book_file)
    
    cover_image_path = None
    if cover_image:
        cover_image_path = os.path.join(BOOK_IMAGE_DIRECTORY, cover_image.filename)
        with open(cover_image_path, "wb") as image_file:
            shutil.copyfileobj(cover_image.file, image_file)
    
    book_data = BookUpdate(
        title=title,
        author_name=author_name,
        description=description,
        categories=categories,
        release_date=release_date,
        file=file_path,
        cover_image=cover_image_path
    )
    result = update_book(book_id, book_data)
    if "No book found" in result:
        raise HTTPException(status_code=404, detail=result)
    return result

@app.delete("/books/{book_id}")
def delete_book_endpoint(book_id: int):
    result = delete_book(book_id)
    if "No book found" in result:
        raise HTTPException(status_code=404, detail=result)
    return result

@app.post("/books/search")
def search_book_endpoint(query: BookQuery):
    return search_book(query)


