from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId

class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int

class Book(BookCreate):
    id: PydanticObjectId = Field(alias="_id")

    class Config:
        # дозволяє відповідати полю "id" до Mongo "_id"
        allow_population_by_field_name = True
        # серіалізує ObjectId у рядок
        json_encoders = {
            PydanticObjectId: str
        }
