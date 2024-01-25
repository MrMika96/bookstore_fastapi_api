from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from books import crud as books_crud, schemas as books_schemas
from db.base_class import Base
from users import crud as users_crud, schemas as users_schemas
from db.session import SessionLocal, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = users_crud.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = users_crud.fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.post("/users/", response_model=users_schemas.User)
def create_user(user: users_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = users_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users_crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[users_schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = users_crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=users_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/books/", response_model=books_schemas.Book)
def create_book_for_user(
    user_id: int, item: books_schemas.BookCreate, db: Session = Depends(get_db)
):
    return books_crud.create_user_book(db=db, item=item, user_id=user_id)


@app.get("/books/", response_model=list[books_schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = books_crud.get_books(db, skip=skip, limit=limit)
    return books
