'''
scraper.py

このモジュールでは、Google Places API を使って博多駅周辺の指定キーワードに該当する場所情報を取得し、Supabase の `place` テーブルに格納します。

事前準備:
1) pip install googlemaps supabase
2) .streamlit/secrets.toml に以下を設定:
   SUPABASE_URL = "https://pszefvosagdpzilocerq.supabase.co"
   SUPABASE_KEY = "<YOUR_SUPABASE_SERVICE_ROLE_KEY>"
   GOOGLE_MAPS_API_KEY = "<YOUR_GOOGLE_MAPS_API_KEY>"

'''  
import os
from googlemaps import Client as GoogleMaps
from supabase import create_client, Client

# 環境変数 or Streamlit secrets 経由で取得
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Supabase クライアント
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# Google Maps API クライアント
gmaps = GoogleMaps(key=GOOGLE_MAPS_API_KEY)

# 博多駅の緯度経度
CENTER_LOCATION = (33.5902, 130.4203)
# 検索キーワードリスト
KEYWORDS = ["カフェ", "リラクゼーション", "エンタメ", "ショッピング"]
# 検索範囲（メートル）
RADIUS = 500


def scrape_and_store(keywords=KEYWORDS, center=CENTER_LOCATION, radius=RADIUS):
    """
    Google Places API を使ってキーワードごとに場所情報を取得し、
    Supabase の `place` テーブルに登録します。
    """
    # 既存の place テーブルをクリアしたい場合は以下を有効化してください
    # supabase.table("place").delete().neq("id", 0).execute()

    for kw in keywords:
        # Nearby Search
        response = gmaps.places_nearby(
            location=center,
            radius=radius,
            keyword=kw,
            language="ja"
        )
        for p in response.get("results", []):
            name = p.get("name")
            vicinity = p.get("vicinity", "")
            lat = p["geometry"]["location"]["lat"]
            lon = p["geometry"]["location"]["lng"]
            place_id = p.get("place_id")
            # Place Details で URL を取得（オプション）
            url = ""
            try:
                details = gmaps.place(place_id=place_id, language="ja")
                url = details.get("result", {}).get("url", "")
            except Exception:
                pass

            record = {
                "name": name,
                "url": url or vicinity,
                "lat": lat,
                "lon": lon,
                "mood": kw,
                # 時間帯が分かれば設定可
                "time": None
            }
            supabase.table("place_duplicate").insert(record).execute()
    print("✅ Supabase にスクレイピング結果を格納しました。")


if __name__ == '__main__':
    scrape_and_store()