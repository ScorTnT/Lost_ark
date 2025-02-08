import requests
import loaAPI

API_KEY = loaAPI.code
BASE_URL = "https://developer-lostark.game.onstove.com"

# 벌목 전리품 카테고리 (90300)
# 재련 재료 카테고리 (50010)
def search_item_name(keyword):
    """로스트아크 API에서 특정 키워드로 아이템 검색"""
    url = f"{BASE_URL}/markets/items"
    headers = {
        "accept": "application/json",
        "authorization": f"bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "Sort": "PRICE",
        "CategoryCode": 50010,  # 벌목 전리품 카테고리
        "ItemName": keyword,  # 검색어
        "PageNo": 1
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        for item in data.get("Items", []):
            print(f"🔍 검색 결과: {item['Name']} | ID: {item['Id']} | 최저가: {item['CurrentMinPrice']}골드")
    else:
        print(f"❌ API 요청 실패 (응답 코드 {response.status_code})")

# 아비도스 융화 재료의 ID 찾기
search_item_name("아비도스 융화 재료")