import os
from fastapi import FastAPI, HTTPException, Response, status
from typing import List
from bson import ObjectId
import motor.motor_asyncio
from pydantic_mongo import PydanticObjectId


from .schemas import Book, BookCreate

app = FastAPI(title="Library API (FastAPI + MongoDB)")

# Підключення до MongoDB через Motor
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://mongo_admin:password@localhost:27017/library"
)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()
collection = db.get_collection("books")

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate):
    doc = payload.dict()
    result = await collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc

@app.get("/books", response_model=List[Book])
async def get_books():
    # отримуємо всі документи
    items = [doc async for doc in collection.find({})]
    return items

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    # валідація ObjectId
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID")
    doc = await collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Book not found")
    return doc

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str):
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID")
    result = await collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def main():
    import uvicorn
    uvicorn.run("library_api.main:app", host="0.0.0.0", port=8000, reload=True)
