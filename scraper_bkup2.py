import os
import sys
import math
import requests
from dotenv import load_dotenv
from googlemaps import Client as GoogleMaps

# .env を探して環境変数に読み込む\
load_dotenv()

# 環境変数から取得
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not GOOGLE_MAPS_API_KEY:
    print("ERROR: 環境変数 GOOGLE_MAPS_API_KEY を設定してください。")
    sys.exit(1)

gmaps = GoogleMaps(key=GOOGLE_MAPS_API_KEY)

# サポートするキーワード
KEYWORDS = ["カフェ", "リラクゼーション", "エンタメ", "ショッピング"]


def haversine(lat1, lon1, lat2, lon2):
    """
    2点間の距離をメートルで返す（ハーサイン距離）
    """
    R = 6371000  # 地球半径 (m)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


def get_current_location():
    print("現在地の取得方法を選択してください:")
    print("  1: IP-API から自動取得")
    print("  2: 自由記述で場所キーワード入力 (例: 博多駅)")
    choice = input("選択 (1 or 2): ")

    if choice == '1':
        try:
            resp = requests.get("http://ip-api.com/json/").json()
            return resp['lat'], resp['lon']
        except Exception as e:
            print("IP-API から現在地取得に失敗しました:", e)
            sys.exit(1)
    else:
        keyword = input("駅名やランドマークを入力してください: ")
        try:
            geocode_result = gmaps.geocode(keyword, language="ja")
        except Exception as e:
            print("ジオコーディングでエラーが発生しました:", e)
            sys.exit(1)
        if not geocode_result:
            print("場所のジオコーディングに失敗しました。プログラムを終了します。")
            sys.exit(1)
        loc = geocode_result[0]['geometry']['location']
        return loc['lat'], loc['lng']


def main():
    print(f"対応キーワード: {', '.join(KEYWORDS)}")
    keyword = input("キーワードを入力してください: ")
    if keyword not in KEYWORDS:
        print("無効なキーワードです。プログラムを終了します。")
        sys.exit(1)

    try:
        time_choice = int(input("時間を入力してください (30, 60, 120 分): "))
    except ValueError:
        print("数値で入力してください。プログラムを終了します。")
        sys.exit(1)

    if time_choice == 30:
        min_r, max_r = 0, 500
    elif time_choice == 60:
        min_r, max_r = 500, 1000
    elif time_choice == 120:
        min_r, max_r = 1000, 2000
    else:
        print("無効な時間選択です。プログラムを終了します。")
        sys.exit(1)

    lat, lon = get_current_location()
    print(f"現在地: (lat: {lat}, lon: {lon})")

    # max_r メートル以内のスポットを検索
    resp = gmaps.places_nearby(location=(lat, lon), radius=max_r, keyword=keyword, language="ja")
    spots = []

    for p in resp.get('results', []):
        loc = p['geometry']['location']
        dist = haversine(lat, lon, loc['lat'], loc['lng'])
        if min_r <= dist <= max_r:
            spots.append({
                'name': p.get('name'),
                'vicinity': p.get('vicinity'),
                'distance_m': int(dist)
            })
        if len(spots) >= 5:
            break

    if not spots:
        print("条件に合う場所が見つかりませんでした。")
        return

    print("\nおすすめの場所 (上位5件):")
    for i, s in enumerate(spots, start=1):
        print(f"{i}. {s['name']} - {s['vicinity']} ({s['distance_m']}m)")


if __name__ == '__main__':
    main()
