from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

books_db = []
current_id = 1

class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    summary: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    summary: Optional[str] = None

@app.get("/books", response_model=List[dict])
def get_books():
    return books_db

@app.post("/books", status_code=201)
def create_book(book: BookCreate):
    global current_id
    new_book = {
        "id": current_id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "summary": book.summary
    }
    books_db.append(new_book)
    current_id += 1
    return {"message": "Book created successfully", "book": new_book}

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.patch("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    for book in books_db:
        if book["id"] == book_id:
            if book_update.title is not None:
                book["title"] = book_update.title
            if book_update.author is not None:
                book["author"] = book_update.author
            if book_update.year is not None:
                book["year"] = book_update.year
            if book_update.summary is not None:
                book["summary"] = book_update.summary
            return {"message": "Book updated successfully", "book": book}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            deleted_book = books_db.pop(index)
            return {"message": "Book deleted successfully", "book": deleted_book}
    raise HTTPException(status_code=404, detail="Book not found")