
import os
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId
import motor.motor_asyncio
from pydantic import BaseModel

from .schemas import Book, BookCreate

app = FastAPI(title="Library API (with JWT Auth + MongoDB)")

# MongoDB setup
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://mongo_admin:password@mongo:27017/library?authSource=admin"
)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()
collection = db.get_collection("books")

# --- JWT / Auth config ---
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fake user store
fake_users_db = {
    "user1": {
        "username": "user1",
        "full_name": "User One",
        "hashed_password": pwd_context.hash("password1"),
        "disabled": False,
    }
}

# --- Pydantic models for auth ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

# --- utility functions ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str) -> Optional[User]:
    user = fake_users_db.get(username)
    return User(**user) if user else None

def authenticate_user(username: str, password: str) -> Optional[User]:
    user_dict = fake_users_db.get(username)
    if not user_dict or not verify_password(password, user_dict["hashed_password"]):
        return None
    return User(**user_dict)

def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(username: str) -> str:
    return create_token(
        {"sub": username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "access"
    )

def create_refresh_token(username: str) -> str:
    return create_token(
        {"sub": username},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "refresh"
    )

# --- dependencies ---
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise JWTError()
        username: str = payload.get("sub")
        if username is None:
            raise JWTError()
    except JWTError:
        raise credentials_exception

    user = get_user(username)
    if not user or user.disabled:
        raise credentials_exception
    return user

# --- auth endpoints ---
@app.post("/token", response_model=Token)
async def login_for_tokens(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(
        access_token=create_access_token(user.username),
        refresh_token=create_refresh_token(user.username),
    )

@app.post("/refresh", response_model=Token)
async def refresh_tokens(body: RefreshRequest):
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise JWTError()
        username: str = payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user(username)
    if not user or user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    return Token(
        access_token=create_access_token(username),
        refresh_token=create_refresh_token(username),
    )

# --- protected CRUD endpoints ---
@app.post(
    "/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    payload: BookCreate,
    current_user: User = Depends(get_current_user),
):
    doc = payload.dict()
    result = await collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return Book(**doc)

@app.get("/books", response_model=List[Book])
async def get_books(current_user: User = Depends(get_current_user)):
    docs = await collection.find({}).to_list(length=None)
    return [Book(**d) for d in docs]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(
    book_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID")
    doc = await collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return Book(**doc)

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID")
    result = await collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- entrypoint ---
def main():
    import uvicorn
    uvicorn.run("library_api.main:app", host="0.0.0.0", port=8000, reload=True)
