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

def calculate_profit(output_name, crafting_cost=352, output_quantity=10, fee_rate=0.05, trade_unit=100):
    """재료를 구매하여 제작 후 판매 시 이득 계산"""
    item_prices = {}  # 📌 가격 캐싱 (최적화)
    
    # ✅ 재료 가격 조회 & 구매 비용 계산
    total_material_cost = 0
    required_materials = {
        "재료1": 86,  # 목재
        "재료2": 45,  # 부드러운 목재
        "재료3": 33   # 아비도스 목재
    }

    for material, needed_per_craft in required_materials.items():
        item_id = ITEM_ID_MAP.get(material)
        category_code = CATEGORY_CODE_MAP.get(material)

        if item_id is None:
            print(f"❌ {material}의 아이템 ID를 찾을 수 없습니다.")
            return
        
        # ✅ 가격을 한 번만 가져오도록 최적화 (페이지 탐색 포함)
        item_prices[material] = get_item_price(item_id, category_code)

        price_per_100 = item_prices[material]
        if price_per_100 is None:
            print(f"❌ {material}의 가격을 불러오지 못했습니다.")
            return
        
        # ✅ 1개당 가격 계산
        price_per_unit = price_per_100 / 100
        
        # ✅ 1회 제작에 사용되는 비용 계산
        cost_per_craft = price_per_unit * needed_per_craft
        total_material_cost += cost_per_craft

    # ✅ 완성품 가격 조회 (페이지 탐색 포함)
    output_id = ITEM_ID_MAP["완성품"]
    output_category = CATEGORY_CODE_MAP["완성품"]
    output_price = get_item_price(output_id, output_category)
    if output_price is None:
        print(f"❌ {output_name}의 가격을 불러오지 못했습니다.")
        return

    # ✅ 총 제작 횟수 및 제작 가능한 총 개수 계산
    total_crafts = math.floor(total_material_cost / sum(required_materials[m] * (item_prices[m] / 100) for m in required_materials))
    max_craftable = total_crafts * output_quantity

    # ✅ 제작 비용 (총 제작 횟수 반영)
    total_crafting_cost = total_crafts * crafting_cost

    # ✅ 제작 후 판매 수익 (출력 개수 * 개당 가격 * 0.95)
    crafting_revenue = (max_craftable * output_price * (1 - fee_rate))

    # ✅ 순이익 계산 (제작 후 판매 수익 - 총 투자 비용)
    net_profit = crafting_revenue - total_material_cost - total_crafting_cost

    print("\n🔍 **비교 결과**")
    print(f"✅ 총 재료 구매 비용: {total_material_cost:.2f} 골드 (1개당 가격 반영)")
    print(f"✅ 제작 비용 (총 {total_crafts}회 제작): {total_crafting_cost} 골드")
    print(f"✅ 총 투자 비용: {total_material_cost + total_crafting_cost:.2f} 골드")
    print(f"✅ 제작 후 판매 수익: {crafting_revenue:.2f} 골드 (수수료 5% 차감)")
    print(f"✅ 순이익: {net_profit:.2f} 골드")

    if net_profit > 0:
        print(f"\n📢 **재료를 구매해서 제작 후 판매하면 {net_profit:.2f} 골드 이득입니다!**")
    else:
        print(f"\n📢 **재료를 구매해서 제작 후 판매하면 {abs(net_profit):.2f} 골드 손해입니다!**")

# 실행
output_name = "아비도스 융화 재료"
calculate_profit(output_name)
