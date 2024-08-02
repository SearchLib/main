__package__ = "main"

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import validates, declarative_base
from database import Base

import sys
import os

class Book(Base):
    __tablename__ = "Book"

    bookId = Column(Integer, primary_key=True, index=True)
    callNum1 = Column(String(10))
    callNum2 = Column(String(10))
    bookName = Column(String(255))
    writer = Column(String(30))
    published = Column(Integer)

class Library(Base):
    __tablename__ = "Library"

    libId = Column(Integer, primary_key=True, index=True)
    libName = Column(String(30))
    latitude = Column(Float)
    longitude = Column(Float)
    open = Column(String(255))

class Exist(Base):
    __tablename__ = "Exist"

    bookId = Column(Integer, primary_key=True)
    libId = Column(Integer, primary_key=True)

class User(Base):
    __tablename__ = "User"

    userId = Column(Integer, primary_key=True, index=True)
    access = Column(Integer, default = 10)

    def __init__(self, userId, access):
        self.userId = userId
        self.access = access