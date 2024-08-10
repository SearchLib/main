__package__ = "main"

from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from model import Book, Library, Exist, User, Log
from database import SessionLocal
import current_location
import databaseURL
import requests

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 로그인 URL 생성
@app.get('/login')
def login():
    kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={databaseURL.CLIENT_ID}&redirect_uri={databaseURL.REDIRECT_URI}&prompt=login"
    return RedirectResponse(url=kakao_auth_url)

# 인증 코드 받기 및 액세스 토큰 요청
@app.get('/oauth')
def oauth(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get('code')  # 수정된 부분: request.args.get -> request.query_params.get
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

    if(db.query(User).filter(User.userId == user_info.get('id')).first() is None):
        user = User(userId=user_info.get('id'), access=10)
        db.add(user)
        db.commit()
    
    return {"user_info": user_info}

@app.get("/wake/{bookName}")
def getLibrary(bookName: str, request: Request, id: int = Header(None), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userId == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"{id}, User not found")
    if user.access == 0:
        raise HTTPException(status_code=404, detail="Access limit exceeded")
    user.access -= 1
    db.commit()

    book = db.query(Book).filter(Book.bookName == bookName).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    exist = db.query(Exist).filter(Exist.bookId == book.bookId).all()
    libList = []
    location = current_location.get_current_location()
    
    for e in exist:
        library = db.query(Library).filter(Library.libId == e.libId).first()
        if library:
            distance = func.sqrt(func.pow(library.latitude - location['lat'], 2) + func.pow(library.longitude - location['lng'], 2))
            library.distance = distance
            libList.append(library)
    
    libList.sort(key=lambda x: x.distance)
    return {"libraries": [lib.__dict__ for lib in libList]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
