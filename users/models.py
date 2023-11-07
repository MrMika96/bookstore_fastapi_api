from sqlalchemy import (
    Column, Integer,
    String, Boolean
)
from sqlalchemy.orm import relationship

from db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    username = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)

    books = relationship("Book", back_populates="author")

