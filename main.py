__package__ = "main"

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from model import Book, Library, Exist, User
from database import SessionLocal

import sys
import os

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/wake/{bookName}")
def getLibrary(bookName: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.bookName == bookName).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    exist = db.query(Exist).filter(Exist.bookId == book.bookId).all()
    libList = []
    for e in exist:
        lib = db.query(Library).filter(Library.libId == e.libId).first()
        libList.append(lib)
    ##순서 정렬 필요
    return libList