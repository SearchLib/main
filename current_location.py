import requests
import json

def get_current_location():
    try:
        response = requests.get("http://www.geoplugin.net/json.gp")
        data = response.json()

        if 'geoplugin_latitude' in data and 'geoplugin_longitude' in data:
            lat = float(data['geoplugin_latitude'])
            lng = float(data['geoplugin_longitude'])
            return {"lat": lat, "lng": lng}
        else:
            print("위치 정보를 가져올 수 없습니다.")
            return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

location = get_current_location()
if location:
    print(f"현재 위치: 위도 = {location['lat']}, 경도 = {location['lng']}")
else:
    print("현재 위치를 불러올 수 없습니다.")
