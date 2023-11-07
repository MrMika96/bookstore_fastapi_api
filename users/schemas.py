from pydantic import BaseModel

from books.schemas import Book


class UserBase(BaseModel):
    username: str
    full_name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    books: list[Book] = []

    class Config:
        from_attributes = True
