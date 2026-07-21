import streamlit as st
import requests
import random
from datetime import datetime

st.set_page_config(
    page_title="대한민국 축제 추천",
    page_icon="🎉",
    layout="wide"
)

st.title("🎉 대한민국 축제 추천 서비스")
st.caption("한국관광공사 TourAPI")

# Streamlit Secrets
API_KEY = st.secrets["TOUR_API_KEY"]

URL = "https://apis.data.go.kr/B551011/KorService2/searchFestival2"

today = datetime.today().strftime("%Y%m%d")

params = {
    "serviceKey": API_KEY,
    "MobileOS": "ETC",
    "MobileApp": "FestivalApp",
    "_type": "json",
    "numOfRows": "100",
    "pageNo": "1",
    "eventStartDate": today
}


@st.cache_data(ttl=3600)
def get_festivals():
    response = requests.get(URL, params=params, timeout=20)

    if response.status_code != 200:
        st.error(f"HTTP 오류 : {response.status_code}")
        st.text(response.text)
        return []

    data = response.json()

    body = data["response"]["body"]

    if body["items"] == "":
        return []

    return body["items"]["item"]


festivals = get_festivals()

if not festivals:
    st.warning("축제 정보가 없습니다.")
    st.stop()

# ------------------

keyword = st.text_input("🔍 축제 검색")

filtered = festivals

if keyword:

    filtered = [
        x for x in festivals
        if keyword.lower() in x["title"].lower()
    ]

st.write(f"총 {len(filtered)}개의 축제를 찾았습니다.")

st.divider()

# 랜덤 추천

if st.button("🎲 오늘의 랜덤 축제 추천"):

    festival = random.choice(filtered)

    st.success(f"오늘 추천 축제는 **{festival['title']}** 입니다!")

    if festival.get("firstimage"):
        st.image(festival["firstimage"], width=700)

    col1, col2 = st.columns(2)

    with col1:
        st.write("📍 주소")
        st.write(festival.get("addr1", "-"))

    with col2:
        st.write("📅 기간")
        st.write(
            festival.get("eventstartdate", "-"),
            "~",
            festival.get("eventenddate", "-")
        )

    st.info(random.choice([
        "📸 사진 찍기 좋은 축제입니다.",
        "❤️ 커플 여행 추천!",
        "👨‍👩‍👧 가족 여행 추천!",
        "🍜 먹거리가 풍부한 축제입니다.",
        "🔥 올해 인기 축제입니다."
    ]))

st.divider()

st.subheader("📋 축제 목록")

for festival in filtered:

    with st.container():

        col1, col2 = st.columns([1,3])

        with col1:

            if festival.get("firstimage"):
                st.image(festival["firstimage"], width=170)

        with col2:

            st.markdown(f"### {festival['title']}")

            st.write(
                f"📅 {festival.get('eventstartdate','')} ~ {festival.get('eventenddate','')}"
            )

            st.write(
                f"📍 {festival.get('addr1','주소 없음')}"
            )

            if festival.get("tel"):
                st.write(
                    f"☎ {festival['tel']}"
                )

        st.divider()
