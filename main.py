from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

books_db = []
current_id = 1

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

@app.get("/books", response_model=List[dict])
def get_books():
    return books_db

@app.post("/books", status_code=201)
def create_book(book: BookCreate):
    global current_id
    new_book = {"id": current_id, **book.dict()}
    books_db.append(new_book)
    current_id += 1
    return new_book

@app.get("/books/{book_id}")
def get_book(book_id: int):
    return books_db[book_id - 1]