from flask import Flask, redirect, request
import requests
import json
import databaseURL
app = Flask(__name__)

# 로그인 URL 생성
@app.route('/login')
def login():
    kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={databaseURL.CLIENT_ID}&redirect_uri={databaseURLREDIRECT_URI}"
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
