import streamlit as st
import requests
import random

# Streamlit Cloud에서는 secrets.toml에 저장
API_KEY = st.secrets["TOUR_API_KEY"]

st.title("🎲 오늘의 랜덤 축제")

url = "https://apis.data.go.kr/B551011/KorService1/searchFestival1"

params = {
    "serviceKey": API_KEY,
    "MobileOS": "ETC",
    "MobileApp": "FestivalApp",
    "_type": "json",
    "eventStartDate": "20260101",
    "numOfRows": 100,
    "pageNo": 1
}

response = requests.get(url, params=params)

if response.status_code == 200:

    data = response.json()

    items = data["response"]["body"]["items"]["item"]

    if st.button("🎲 랜덤 추천 받기"):

        festival = random.choice(items)

        st.success(f"오늘의 추천 축제는 **{festival['title']}** 입니다!")

        if festival.get("firstimage"):
            st.image(festival["firstimage"], use_container_width=True)

        st.write("📍 주소")
        st.write(festival.get("addr1", "정보 없음"))

        st.write("📅 행사 시작")
        st.write(festival.get("eventstartdate"))

        st.write("📅 행사 종료")
        st.write(festival.get("eventenddate"))

        reasons = [
            "사진 찍기 좋은 축제입니다 📸",
            "가족과 함께 가기 좋아요 👨‍👩‍👧",
            "커플 데이트 코스로 추천 ❤️",
            "먹거리가 다양한 축제입니다 🍜",
            "SNS에서 인기 있는 축제입니다 🔥",
            "혼자 여행해도 즐길 수 있어요 🚶"
        ]

        st.info(random.choice(reasons))

else:
    st.error("축제 정보를 가져오지 못했습니다.")
