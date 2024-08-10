__package__ = "main"

from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import validates, declarative_base
from database import Base
import datetime

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

    userId = Column(BigInteger, primary_key=True, index=True)
    access = Column(Integer, default = 10)

class Log(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    client_ip = Column(String, index=True)
    method = Column(String)
    url = Column(String)
    status_code = Column(Integer)
    process_time = Column(Float)
    timestamp = Column(String, default=datetime.datetime.now())
