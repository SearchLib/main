__package__ = "main"

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import validates, declarative_base
from database import Base

import sys
import os

class Book(Base):
    __tablename__ = "Book"

class Library(Base):
    __tablename__ = "Library"

class Exist(Base):
    __tablename__ = "Exist"

class User(Base):
    __tablename__ = "User"