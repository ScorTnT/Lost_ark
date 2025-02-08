import requests
import math
import loaAPI

API_KEY = loaAPI.code
BASE_URL = "https://developer-lostark.game.onstove.com"

# ✅ 정확한 ID 반영
ITEM_ID_MAP = {
    "재료1": 6882301,  # 목재
    "재료2": 6882304,  # 부드러운 목재
    "재료3": 6884308,  # 아비도스 목재
    "완성품": 6861012   # ✅ 아비도스 융화 재료
}

CATEGORY_CODE_MAP = {
    "재료1": 90300,  # 벌목 전리품
    "재료2": 90300,  # 벌목 전리품
    "재료3": 90300,  # 벌목 전리품
    "완성품": 50010   # 재련 재료
}

def find_item_page(item_id, category_code):
    """아이템이 어느 PageNo에 있는지 자동으로 찾는 함수"""
    page = 1
    url = f"{BASE_URL}/markets/items"
    headers = {
        "accept": "application/json",
        "authorization": f"bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "Sort": "PRICE",
        "CategoryCode": category_code
    }
    while True:
        payload["PageNo"] = page

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            if not data.get("Items"):  # 더 이상 아이템이 없으면 종료
                return None
            for item in data.get("Items", []):
                if item["Id"] == item_id:
                    print(f"✅ {item['Name']} | 최저가: {item['CurrentMinPrice']}골드")
                    return page  # 페이지 번호 반환
            page += 1  # 다음 페이지로 이동
        else:
            print(f"❌ API 요청 실패 (응답 코드 {response.status_code})")
            return None

def get_item_price(item_id, category_code):
    """아이템 가격 조회 (PageNo 자동 탐색)"""
    page_no = find_item_page(item_id, category_code)
    if page_no is None:
        print(f"❌ {item_id} (CategoryCode {category_code})를 찾을 수 없습니다.")
        return None

    url = f"{BASE_URL}/markets/items"
    headers = {
        "accept": "application/json",
        "authorization": f"bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "Sort": "PRICE",
        "CategoryCode": category_code,
        "PageNo": page_no
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        for item in data.get("Items", []):
            if item["Id"] == item_id:
                return item["CurrentMinPrice"]  # 최저 가격 반환
    return None

def calculate_profit(materials, output_name, crafting_cost=352, output_quantity=10, fee_rate=0.05, trade_unit=100):
    """제작 vs 즉시 판매 비교"""
    item_prices = {}  # 📌 가격 캐싱 (최적화)
    
    for material, (needed_per_craft, owned) in materials.items():
        item_id = ITEM_ID_MAP.get(material)
        category_code = CATEGORY_CODE_MAP.get(material)

        if item_id is None:
            print(f"❌ {material}의 아이템 ID를 찾을 수 없습니다.")
            return
        
        # ✅ 가격을 한 번만 가져오도록 최적화
        if material not in item_prices:
            item_prices[material] = get_item_price(item_id, category_code)

        price = item_prices[material]
        if price is None:
            print(f"❌ {material}의 가격을 불러오지 못했습니다.")
            return

    # ✅ 완성품 가격 조회
    output_id = ITEM_ID_MAP["완성품"]
    output_category = CATEGORY_CODE_MAP["완성품"]
    output_price = get_item_price(output_id, output_category)
    if output_price is None:
        print(f"❌ {output_name}의 가격을 불러오지 못했습니다.")
        return

    # ✅ 총 제작 횟수 및 제작 가능한 총 개수 계산
    total_crafts = min(
        materials["재료1"][1] // materials["재료1"][0],
        materials["재료2"][1] // materials["재료2"][0],
        materials["재료3"][1] // materials["재료3"][0]
    )
    max_craftable = total_crafts * output_quantity

    # ✅ 제작 비용 (총 제작 횟수 반영)
    total_crafting_cost = total_crafts * crafting_cost

    # ✅ 제작 후 판매 실제 수익
    crafting_revenue = (output_price * max_craftable) * (1 - fee_rate) - total_crafting_cost

    # ✅ 즉시 판매 수익 (100개 단위 가격 적용)
    direct_sell_revenue = (
        (166 * item_prices["재료1"]) +  # ✅ 목재 (100개 단위)
        (83 * item_prices["재료2"]) +   # ✅ 부드러운 목재 (100개 단위)
        (53 * item_prices["재료3"])     # ✅ 아비도스 목재 (100개 단위)
    ) * (1 - fee_rate)  # ✅ 수수료 5% 적용

    print("\n🔍 **비교 결과**")
    print(f"✅ 제작 비용 (총 {total_crafts}회 제작): {total_crafting_cost} 골드")
    print(f"✅ 제작 후 판매 수익 (실제 이익): {crafting_revenue:.2f} 골드 (수수료 및 제작 비용 차감)")
    print(f"✅ 즉시 판매 수익: {direct_sell_revenue:.2f} 골드 (수수료 적용 후)")

    if crafting_revenue > direct_sell_revenue:
        print(f"\n📢 **제작해서 판매하는 것이 {crafting_revenue - direct_sell_revenue:.2f} 골드 더 이득입니다!**")
    else:
        print(f"\n📢 **보유한 재료를 바로 판매하는 것이 {direct_sell_revenue - crafting_revenue:.2f} 골드 더 이득입니다!**")

# 보유한 재료 정보
materials = {
    "재료1": (86, 16689),
    "재료2": (45, 8393),
    "재료3": (33, 2492)
}
output_name = "아비도스 융화 재료"

calculate_profit(materials, output_name)
