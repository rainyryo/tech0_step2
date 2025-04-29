import os
import streamlit as st
from googlemaps import Client as GoogleMaps

# 環境変数／Secrets からキーを取得
api_key = os.getenv("GOOGLE_MAPS_API_KEY") or st.secrets["GOOGLE_MAPS_API_KEY"]
gmaps = GoogleMaps(key=api_key)

# 博多駅の緯度経度
hakata_latlon = (33.5902, 130.4203)

# 「カフェ」キーワードで半径1.5km以内を検索
places = gmaps.places_nearby(
    location=hakata_latlon,
    radius=1500,
    keyword="カフェ"
)

# 結果を表示
for p in places.get("results", []):
    st.write(p["name"], p["vicinity"])
