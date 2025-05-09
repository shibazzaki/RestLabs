# lab_5/library_api/schemas.py

from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId

class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int

class Book(BookCreate):
    id: PydanticObjectId = Field(alias="_id")

    class Config:
        # дозволяє створити Book(id=...) з поля "_id" від Mongo
        allow_population_by_field_name = True
        # серіалізує ObjectId у JSON як рядок
        json_encoders = {
            PydanticObjectId: str
        }
