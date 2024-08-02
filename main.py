__package__ = "main"

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from model import Book, Library, Exist, User
from database import SessionLocal
import current_location
import databaseURL
from flask import Flask, redirect, request
import requests
import json
import datetime
import time

app = Flask(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 로그인 URL 생성
@app.route('/login')
def login():
    kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={databaseURL.CLIENT_ID}&redirect_uri={databaseURL.REDIRECT_URI}"
    return redirect(kakao_auth_url)

# 인증 코드 받기 및 액세스 토큰 요청
@app.route('/oauth')
def oauth():
    code = request.args.get('code')
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": databaseURL.CLIENT_ID,
        "redirect_uri": databaseURL.REDIRECT_URI,
        "code": code,
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    # 액세스 토큰으로 사용자 정보 요청
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()
    
    return f"사용자 정보: {json.dumps(user_info, ensure_ascii=False)}"


@app.route("/wake/{bookName}")
def getLibrary(bookName: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.bookName == bookName).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    exist = db.query(Exist).filter(Exist.bookId == book.bookId).all()
    libList = []
    location = current_location.get_current_location()
    for e in exist:
        distance = func.sqrt(func.pow(Library.latitude - location['lat'], 2) + func.pow(Library.longitude - location['lng'], 2))
        lib = db.query(Library).filter(Library.libId == e.libId).first() + distance
        libList.append(lib)
    libList.sort(key=lambda x: x.distance)
    return libList
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    if request.endpoint != 'static':
        process_time = time.time() - request.start_time
        log_entry = Log(
            client_ip=request.remote_addr,
            method=request.method,
            url=request.path,
            status_code=response.status_code,
            process_time=process_time,
            timestamp=datetime.datetime.now()
        )
        db.session.add(log_entry)
        db.session.commit()
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)