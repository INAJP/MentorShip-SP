from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Library API",
    description="A simple in-memory library management API built with FastAPI.",
    version="1.0.0",
)

books_db: List[dict] = []
current_id = 1


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(gt=0)
    summary: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    author: Optional[str] = Field(default=None, min_length=1)
    year: Optional[int] = Field(default=None, gt=0)
    summary: Optional[str] = None

    @field_validator("title", "author", "year")
    @classmethod
    def required_fields_cannot_be_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value


class Book(BookCreate):
    id: int


class BookResponse(BaseModel):
    message: str
    book: Book


def find_book(book_id: int) -> dict:
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books", response_model=List[Book])
def get_books():
    return books_db


@app.post("/books", status_code=201, response_model=BookResponse)
def create_book(book: BookCreate):
    global current_id
    new_book = {"id": current_id, **book.model_dump()}
    books_db.append(new_book)
    current_id += 1
    return {"message": "Book created successfully", "book": new_book}


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    return find_book(book_id)


@app.patch("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate):
    book = find_book(book_id)
    book.update(book_update.model_dump(exclude_unset=True))
    return {"message": "Book updated successfully", "book": book}


@app.delete("/books/{book_id}", response_model=BookResponse)
def delete_book(book_id: int):
    book = find_book(book_id)
    books_db.remove(book)
    return {"message": "Book deleted successfully", "book": book}