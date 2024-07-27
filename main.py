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
    ##현재 유저의 access가 0이면 return
    book = db.query(Book).filter(Book.bookName == bookName).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    exist = db.query(Exist).filter(Exist.bookId == book.bookId).all()
    libList = []
    for e in exist:
        distance = func.sqrt(func.pow(Library.latitude - 37.5665, 2) + func.pow(Library.longitude - 126.9780, 2))
        ##임시 현재 위치
        lib = db.query(Library).filter(Library.libId == e.libId).first() + distance
        libList.append(lib)
    libList.sort(key=lambda x: x.distance)
    return libList