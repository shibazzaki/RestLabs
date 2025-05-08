from pydantic import BaseModel, Field, validator
from typing import Optional
import datetime

current_year = datetime.datetime.now().year

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    published_year: int = Field(..., ge=0, le=current_year)

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: str
