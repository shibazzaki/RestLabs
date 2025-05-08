import datetime
from fastapi import FastAPI, HTTPException
from uuid import uuid4
from typing import List

from .schemas import Book, BookCreate

app = FastAPI(title="Library API (FastAPI)")

# in-memory storage
books: List[Book] = []

@app.get("/books", response_model=List[Book])
async def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    for b in books:
        if b.id == book_id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", response_model=Book, status_code=201)
async def create_book(payload: BookCreate):
    new_book = Book(id=str(uuid4()), **payload.dict())
    books.append(new_book)
    return new_book

@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: str):
    for idx, b in enumerate(books):
        if b.id == book_id:
            books.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Book not found")

def main():
    import uvicorn
    uvicorn.run("library_api.main:app", host="0.0.0.0", port=8000, reload=True)
