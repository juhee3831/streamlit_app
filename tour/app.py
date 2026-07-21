import streamlit as st
import requests
import random

# Streamlit Cloud Secrets에서 API 키 불러오기
API_KEY = st.secrets["TOUR_API_KEY"]

URL = "https://apis.data.go.kr/B551011/KorService1/searchFestival1"

st.title("🎲 오늘의 랜덤 축제")

params = {
    "serviceKey": API_KEY,
    "MobileOS": "ETC",
    "MobileApp": "FestivalApp",
    "_type": "json",
    "eventStartDate": "20260101",
    "numOfRows": 100,
    "pageNo": 1,
}

try:
    response = requests.get(URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    items = data["response"]["body"]["items"].get("item", [])

    if not items:
        st.warning("현재 조회 가능한 축제가 없습니다.")

    elif st.button("🎲 랜덤 축제 추천"):
        festival = random.choice(items)

        st.subheader(f"🎉 {festival['title']}")

        if festival.get("firstimage"):
            st.image(festival["firstimage"], use_container_width=True)

        st.write(f"📍 **주소** : {festival.get('addr1', '정보 없음')}")
        st.write(f"📅 **기간** : {festival.get('eventstartdate')} ~ {festival.get('eventenddate')}")

        st.success(random.choice([
            "사진 찍기 좋은 축제입니다! 📸",
            "데이트 코스로 추천합니다. ❤️",
            "가족과 함께 즐기기 좋아요. 👨‍👩‍👧",
            "먹거리가 풍부한 축제입니다. 🍜",
            "올해 인기 축제로 기대를 모으고 있습니다. 🔥",
        ]))

except Exception as e:
    st.error(f"오류가 발생했습니다.\n\n{e}")
