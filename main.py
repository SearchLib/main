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

